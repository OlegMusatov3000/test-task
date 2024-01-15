import os

from django.db import models


class BaseFinancialModel(models.Model):
    start_balance_active_value = models.DecimalField(
        verbose_name="Значение: Входящее сальдо | Актив ",
        max_digits=40, decimal_places=2, default=0,
    )
    start_balance_passive_value = models.DecimalField(
        verbose_name="Значение: Входящее сальдо | Пассив ",
        max_digits=40, decimal_places=2, default=0,
    )
    turnover_debit_value = models.DecimalField(
        verbose_name="Значение: Обороты | Дебит ",
        max_digits=40, decimal_places=2, default=0,
    )
    turnover_credit_value = models.DecimalField(
        verbose_name="Значение: Обороты | Кредит ",
        max_digits=40, decimal_places=2, default=0,
    )
    end_balance_active_value = models.DecimalField(
        verbose_name="Значение: Исходящее сальдо | Актив ",
        max_digits=40, decimal_places=2, default=0,
        help_text='Расчитывается автоматически после сохранения'
    )
    end_balance_passive_value = models.DecimalField(
        verbose_name="Итоговое значение: : Исходящее сальдо | Пассив ",
        max_digits=40, decimal_places=2, default=0,
        help_text='Расчитывается автоматически после сохранения'
    )

    class Meta:
        abstract = True

    def calculate_end_balance_active_value(self):
        return self.start_balance_active_value + (self.turnover_debit_value - self.turnover_credit_value)

    def calculate_end_balance_passive_value(self):
        return self.start_balance_passive_value + (self.turnover_credit_value - self.turnover_debit_value)


class Bank(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Наименование банка", unique=True
        )

    class Meta:
        verbose_name = "Банк"
        verbose_name_plural = "Банки"

    def __str__(self):
        return self.name


class BalanceSheet(BaseFinancialModel):
    start_period = models.DateField('Начало отчета', auto_now=False)
    end_period = models.DateField('Конец отчета', auto_now=False)
    bank = models.ForeignKey(
        Bank, on_delete=models.CASCADE,
        verbose_name="Банк", related_name='balance_sheet'
    )
    file = models.FileField(
        upload_to='balance_sheets/', verbose_name="Файл балансовой ведомости"
    )

    class Meta:
        verbose_name = "Балансовая ведомость"
        verbose_name_plural = "Балансовые ведомости"
        constraints = [
            models.UniqueConstraint(
                fields=['start_period', 'end_period', 'bank'],
                name='uniq_balance_sheet'
            )
        ]

    def __str__(self):
        return f"Балансовая ведомость банка: {self.bank} из файла {os.path.basename(self.file.name)}"


class FinancialClass(BaseFinancialModel):

    number = models.SmallIntegerField('Номер класса')
    name = models.CharField(max_length=100, verbose_name="Наименование класса")
    balance_sheet = models.ForeignKey(
        BalanceSheet, on_delete=models.CASCADE,
        verbose_name="Балансовая ведомость", related_name='financial_classes'
    )

    class Meta:
        verbose_name = "Финансовый класс"
        verbose_name_plural = "Финансовые классы"
        ordering = ('number',)
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'name', 'balance_sheet'],
                name='uniq_financial_class'
            )
        ]

    def __str__(self):
        return f'Класс {self.number} {self.name} в {self.balance_sheet}'


class BankAccount(BaseFinancialModel):
    code = models.CharField(
        max_length=4, verbose_name="Код счета"
    )
    financial_class = models.ForeignKey(
        FinancialClass, on_delete=models.CASCADE,
        verbose_name="Финансовый класс", related_name='bank_accounts'
    )

    class Meta:
        verbose_name = "Банковский счет"
        verbose_name_plural = "Банковские счета"
        ordering = ('code',)
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'financial_class'],
                name='uniq_bank_account'
            )
        ]

    def calculate_end_balance_active_value(self):
        end_balance_active_value = self.start_balance_active_value + (
                self.turnover_debit_value - self.turnover_credit_value
            )
        return end_balance_active_value

    def calculate_end_balance_passive_value(self):
        end_balance_passive_value = self.start_balance_passive_value + (
                self.turnover_credit_value - self.turnover_debit_value
            )
        return end_balance_passive_value

    def calculate_news_total_values(self, news_values_in_fields):
        news_total_values = []
        for field in news_values_in_fields:
            news_total_values.append(sum(getattr(account, field) for account in self.financial_class.bank_accounts.all()))
        return news_total_values

    def get_changed_fields(self):
        if self.pk:
            prev_obj = BankAccount.objects.get(id=self.pk)
            return [field.name for field in self._meta.fields if getattr(self, field.name) != getattr(prev_obj, field.name)]
        return [field.name for field in self._meta.fields if field.name not in ['id', 'code', 'financial_class']]

    def save(self, *args, **kwargs):
        if self.start_balance_active_value != 0:
            self.end_balance_active_value = (
                self.calculate_end_balance_active_value()
            )
            self.end_balance_passive_value = 0
        else:
            self.end_balance_passive_value = (
                self.calculate_end_balance_passive_value()
            )
            self.end_balance_active_value = 0

        news_values_in_fields = self.get_changed_fields()
        super().save(*args, **kwargs)

        if news_values_in_fields:
            news_total_values = self.calculate_news_total_values(news_values_in_fields)
            for field_name, new_value in zip(news_values_in_fields, news_total_values):
                setattr(self.financial_class, field_name, new_value)
            self.financial_class.save()

    def __str__(self):
        return f'{self.code} для {self.financial_class}'

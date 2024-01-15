import os
from decimal import Decimal, ROUND_DOWN

from django.db import models
from django.utils.translation import gettext_lazy as _


class Bank(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Наименование банка", unique=True
        )

    class Meta:
        verbose_name = "Банк"
        verbose_name_plural = "Банки"

    def __str__(self):
        return self.name


class BalanceSheet(models.Model):
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


class FinancialClass(models.Model):

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


class BankAccount(models.Model):
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

    def __str__(self):
        return f'{self.code} для {self.financial_class}'


class FinancialGroup(models.Model):

    class GroupName(models.TextChoices):
        '''Имя группы.'''

        START_BALANCE = 'Входящее сальдо', _('Входящее сальдо')
        TURNOVER = 'Обороты', _('Обороты')
        END_BALANCE = 'Исходящее сальдо', _('Исходящее сальдо')

    name = models.CharField(
        'Имя группы', max_length=30, choices=GroupName.choices
    )
    balance_sheet = models.ForeignKey(
        BalanceSheet, on_delete=models.CASCADE,
        verbose_name="Балансовая ведомость", related_name='financial_groups'
    )

    class Meta:
        verbose_name = "Финансовая группа"
        verbose_name_plural = "Финансовые группы"

    def __str__(self):
        return f'{self.name} в {self.balance_sheet}'


class FinancialSubtype(models.Model):

    class SubtypeName(models.TextChoices):
        '''Имя подгруппы.'''

        ACTIVE = 'Актив', _('Актив')
        PASSIVE = 'Пассив', _('Пассив')
        DEBIT = 'Дебит', _('Дебит')
        CREDIT = 'Кредит', _('Кредит')

    name = models.CharField(
        'Имя подгруппы', max_length=30, choices=SubtypeName.choices
    )
    financial_group = models.ForeignKey(
        FinancialGroup, on_delete=models.CASCADE,
        verbose_name="Финансовая группа", related_name='financial_subtypes'
    )

    class Meta:
        verbose_name = "Финансовая подгруппа"
        verbose_name_plural = "Финансовые подгруппы"
        ordering = ('id',)

    def __str__(self):
        return f'{self.name} | {self.financial_group}'


class FinancialStatement(models.Model):
    value = models.DecimalField(
        verbose_name="Значение", max_digits=40, decimal_places=2
    )
    financial_subtype = models.ForeignKey(
        FinancialSubtype, on_delete=models.CASCADE,
        verbose_name="Финансовая подгруппа",
        related_name='financial_statements')
    bank_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE,
        verbose_name="Банковский счет",
        related_name='financial_statements')

    class Meta:
        verbose_name = "Финансовая отчетность"
        verbose_name_plural = "Финансовые отчетности"
        ordering = ('financial_subtype',)
        constraints = [
            models.UniqueConstraint(
                fields=['value', 'financial_subtype', 'bank_account'],
                name='uniq_financial_statement'
            )
        ]

    def save(self, *args, **kwargs):
        if self.financial_subtype.financial_group.name != FinancialGroup.GroupName.END_BALANCE.value:
            if self.financial_subtype.name == FinancialSubtype.SubtypeName.ACTIVE:
                name_financial_group = FinancialSubtype.SubtypeName.ACTIVE
            if self.financial_subtype.name == FinancialSubtype.SubtypeName.PASSIVE:
                name_financial_group = FinancialSubtype.SubtypeName.PASSIVE
            # if self.financial_subtype.name == FinancialSubtype.SubtypeName.CREDIT:
            #     name_financial_group = FinancialSubtype.SubtypeName.ACTIVE
            if self.value == 0:
                value = 0
            else:
                turnover_financial_group, _ = FinancialGroup.objects.get_or_create(
                    name=FinancialGroup.GroupName.TURNOVER.value,
                    balance_sheet=self.bank_account.financial_class.balance_sheet
                )
                debit_financial_subtype, _ = FinancialSubtype.objects.get_or_create(
                    name=FinancialSubtype.SubtypeName.DEBIT.value,
                    financial_group=turnover_financial_group
                )
                credit_financial_subtype, _ = FinancialSubtype.objects.get_or_create(
                    name=FinancialSubtype.SubtypeName.CREDIT.value,
                    financial_group=turnover_financial_group
                )
                debit_value = FinancialStatement.objects.filter(
                    financial_subtype=debit_financial_subtype,
                    bank_account=self.bank_account
                ).first()
                if debit_value:
                    debit_value = debit_value.value
                else:
                    debit_value = 0
                credit_value = FinancialStatement.objects.filter(
                    financial_subtype=credit_financial_subtype,
                    bank_account=self.bank_account
                ).first()
                if credit_value:
                    credit_value = credit_value.value
                else:
                    credit_value = 0
                value = self.value + (debit_value - credit_value)
            financial_group, _ = FinancialGroup.objects.get_or_create(
                name=FinancialGroup.GroupName.END_BALANCE.value,
                balance_sheet=self.bank_account.financial_class.balance_sheet
            )

            financial_subtype, _ = FinancialSubtype.objects.get_or_create(
                name=name_financial_group,
                financial_group=financial_group
            )
            if not self.pk:
                FinancialStatement.objects.create(
                    value=value,
                    financial_subtype=financial_subtype,
                    bank_account=self.bank_account
                )
            else:
                obj = FinancialStatement.objects.filter(
                    value=FinancialStatement.objects.get(pk=self.pk).value,
                    financial_subtype=financial_subtype,
                    bank_account=self.bank_account
                ).first()
                if obj:
                    obj.value = value

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bank_account} | {self.financial_subtype}: {self.value}"

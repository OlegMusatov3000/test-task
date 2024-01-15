# Generated by Django 5.0.1 on 2024-01-15 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Наименование банка')),
            ],
            options={
                'verbose_name': 'Банк',
                'verbose_name_plural': 'Банки',
            },
        ),
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_balance_active_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Входящее сальдо | Актив ')),
                ('start_balance_passive_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Входящее сальдо | Пассив ')),
                ('turnover_debit_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Обороты | Дебит ')),
                ('turnover_credit_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Обороты | Кредит ')),
                ('end_balance_active_value', models.DecimalField(decimal_places=2, default=0, help_text='Расчитывается автоматически после сохранения', max_digits=40, verbose_name='Значение: Исходящее сальдо | Актив ')),
                ('end_balance_passive_value', models.DecimalField(decimal_places=2, default=0, help_text='Расчитывается автоматически после сохранения', max_digits=40, verbose_name='Итоговое значение: : Исходящее сальдо | Пассив ')),
                ('start_period', models.DateField(verbose_name='Начало отчета')),
                ('end_period', models.DateField(verbose_name='Конец отчета')),
                ('file', models.FileField(upload_to='balance_sheets/', verbose_name='Файл балансовой ведомости')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balance_sheet', to='osv.bank', verbose_name='Банк')),
            ],
            options={
                'verbose_name': 'Балансовая ведомость',
                'verbose_name_plural': 'Балансовые ведомости',
            },
        ),
        migrations.CreateModel(
            name='FinancialClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_balance_active_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Входящее сальдо | Актив ')),
                ('start_balance_passive_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Входящее сальдо | Пассив ')),
                ('turnover_debit_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Обороты | Дебит ')),
                ('turnover_credit_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Обороты | Кредит ')),
                ('end_balance_active_value', models.DecimalField(decimal_places=2, default=0, help_text='Расчитывается автоматически после сохранения', max_digits=40, verbose_name='Значение: Исходящее сальдо | Актив ')),
                ('end_balance_passive_value', models.DecimalField(decimal_places=2, default=0, help_text='Расчитывается автоматически после сохранения', max_digits=40, verbose_name='Итоговое значение: : Исходящее сальдо | Пассив ')),
                ('number', models.SmallIntegerField(verbose_name='Номер класса')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование класса')),
                ('balance_sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financial_classes', to='osv.balancesheet', verbose_name='Балансовая ведомость')),
            ],
            options={
                'verbose_name': 'Финансовый класс',
                'verbose_name_plural': 'Финансовые классы',
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='JointBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_balance_active_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Входящее сальдо | Актив ')),
                ('start_balance_passive_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Входящее сальдо | Пассив ')),
                ('turnover_debit_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Обороты | Дебит ')),
                ('turnover_credit_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Обороты | Кредит ')),
                ('end_balance_active_value', models.DecimalField(decimal_places=2, default=0, help_text='Расчитывается автоматически после сохранения', max_digits=40, verbose_name='Значение: Исходящее сальдо | Актив ')),
                ('end_balance_passive_value', models.DecimalField(decimal_places=2, default=0, help_text='Расчитывается автоматически после сохранения', max_digits=40, verbose_name='Итоговое значение: : Исходящее сальдо | Пассив ')),
                ('code', models.CharField(max_length=2, verbose_name='Объединенный код счета')),
                ('financial_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joint_bank_accounts', to='osv.financialclass', verbose_name='Финансовый класс')),
            ],
            options={
                'verbose_name': 'Объединенный банковский счет',
                'verbose_name_plural': 'Объединенные банковские счета',
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_balance_active_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Входящее сальдо | Актив ')),
                ('start_balance_passive_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Входящее сальдо | Пассив ')),
                ('turnover_debit_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Обороты | Дебит ')),
                ('turnover_credit_value', models.DecimalField(decimal_places=2, default=0, max_digits=40, verbose_name='Значение: Обороты | Кредит ')),
                ('end_balance_active_value', models.DecimalField(decimal_places=2, default=0, help_text='Расчитывается автоматически после сохранения', max_digits=40, verbose_name='Значение: Исходящее сальдо | Актив ')),
                ('end_balance_passive_value', models.DecimalField(decimal_places=2, default=0, help_text='Расчитывается автоматически после сохранения', max_digits=40, verbose_name='Итоговое значение: : Исходящее сальдо | Пассив ')),
                ('code', models.CharField(max_length=4, verbose_name='Код счета')),
                ('joint_bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_accounts', to='osv.jointbankaccount', verbose_name='Объединенный банковский счет')),
            ],
            options={
                'verbose_name': 'Банковский счет',
                'verbose_name_plural': 'Банковские счета',
                'ordering': ('code',),
            },
        ),
        migrations.AddConstraint(
            model_name='balancesheet',
            constraint=models.UniqueConstraint(fields=('start_period', 'end_period', 'bank'), name='uniq_balance_sheet'),
        ),
        migrations.AddConstraint(
            model_name='financialclass',
            constraint=models.UniqueConstraint(fields=('number', 'name', 'balance_sheet'), name='uniq_financial_class'),
        ),
        migrations.AddConstraint(
            model_name='jointbankaccount',
            constraint=models.UniqueConstraint(fields=('code', 'financial_class'), name='uniq_joint_bank_account'),
        ),
        migrations.AddConstraint(
            model_name='bankaccount',
            constraint=models.UniqueConstraint(fields=('code', 'joint_bank_account'), name='uniq_bank_account'),
        ),
    ]

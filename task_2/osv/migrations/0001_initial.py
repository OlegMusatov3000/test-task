# Generated by Django 5.0.1 on 2024-01-15 02:27

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
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, verbose_name='Код счета')),
                ('value_1', models.DecimalField(decimal_places=2, max_digits=40, verbose_name='Значение')),
                ('value_2', models.DecimalField(decimal_places=2, max_digits=40, verbose_name='Значение')),
                ('value_3', models.DecimalField(decimal_places=2, max_digits=40, verbose_name='Значение')),
                ('value_4', models.DecimalField(decimal_places=2, max_digits=40, verbose_name='Значение')),
                ('value_5', models.DecimalField(decimal_places=2, max_digits=40, verbose_name='Значение')),
                ('value_6', models.DecimalField(decimal_places=2, max_digits=40, verbose_name='Значение')),
                ('financial_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_accounts', to='osv.financialclass', verbose_name='Финансовый класс')),
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
            model_name='bankaccount',
            constraint=models.UniqueConstraint(fields=('code', 'financial_class'), name='uniq_bank_account'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-01-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osv', '0004_financialclass_end_balance_passive_value_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialclass',
            name='end_balance_passive_value',
        ),
        migrations.AddField(
            model_name='financialclass',
            name='total_class_end_balance_passive_value',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Расчитывается автоматически после сохранения', max_digits=40, verbose_name='Итоговое значение по классу: : Исходящее сальдо | Пассив '),
        ),
    ]

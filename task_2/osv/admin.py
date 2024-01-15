from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Bank, BalanceSheet, FinancialClass, JointBankAccount, BankAccount,
)


admin.site.unregister(Group)

admin.site.register(Bank)


@admin.register(BalanceSheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    list_display = list_display_links = (
        'start_period', 'end_period', 'bank', 'file', 'show_data_link'
    )
    search_fields = ('bank__name',)
    list_filter = ('start_period', 'end_period')
    readonly_fields = (
        'start_balance_active_value',
        'start_balance_passive_value',
        'turnover_debit_value',
        'turnover_credit_value',
        'end_balance_active_value',
        'end_balance_passive_value'
    )

    def show_data_link(self, obj):
        url = reverse('show_data', args=[obj.id])
        return format_html('<a href="{}">Показать данные</a>', url)

    show_data_link.short_description = "Показать данные этой ведомости"


@admin.register(FinancialClass)
class FinancialClassAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('number', 'name', 'balance_sheet')
    search_fields = ('number', 'name')
    list_filter = ('balance_sheet',)
    readonly_fields = (
        'start_balance_active_value',
        'start_balance_passive_value',
        'turnover_debit_value',
        'turnover_credit_value',
        'end_balance_active_value',
        'end_balance_passive_value'
    )


@admin.register(JointBankAccount)
class JointBankAccountAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('code', 'financial_class')
    search_fields = ('code',)
    list_filter = ('financial_class',)
    readonly_fields = (
        'start_balance_active_value',
        'start_balance_passive_value',
        'turnover_debit_value',
        'turnover_credit_value',
        'end_balance_active_value',
        'end_balance_passive_value'
    )


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('code', 'joint_bank_account')
    search_fields = ('code',)
    list_filter = ('joint_bank_account',)
    readonly_fields = (
        'end_balance_active_value', 'end_balance_passive_value'
    )

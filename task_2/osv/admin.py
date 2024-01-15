from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Bank, BalanceSheet, FinancialClass, BankAccount,
    FinancialGroup, FinancialSubtype, FinancialStatement
)


admin.site.unregister(Group)

admin.site.register(Bank)
admin.site.register(FinancialClass)
admin.site.register(BankAccount)
admin.site.register(FinancialGroup)
admin.site.register(FinancialSubtype)
admin.site.register(FinancialStatement)


@admin.register(BalanceSheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    list_display = list_display_links = [
        'start_period', 'end_period', 'bank', 'file', 'show_data_link'
    ]
    search_fields = ('bank',)

    list_filter = ('start_period', 'end_period')

    def show_data_link(self, obj):
        url = reverse('show_data', args=[obj.id])
        return format_html('<a href="{}">Показать данные</a>', url)

    show_data_link.short_description = "Показать данные этой ведомости"

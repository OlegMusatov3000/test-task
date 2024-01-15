from django.db.models.signals import pre_delete
from django.dispatch import receiver

from osv.models import BankAccount, BaseFinancialModel


@receiver(pre_delete, sender=BankAccount)
def bank_account_pre_delete(sender, instance, **kwargs):
    financial_fields = [
        field.name for field in BaseFinancialModel._meta.fields
    ]

    for field in financial_fields:
        value = getattr(instance, field)
        setattr(
            instance.joint_bank_account,
            field,
            getattr(instance.joint_bank_account, field) - value
        )

    instance.joint_bank_account.save(update_fields=[*financial_fields])

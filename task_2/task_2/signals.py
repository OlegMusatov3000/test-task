from django.db.models.signals import pre_delete
from django.dispatch import receiver

from osv.models import BankAccount, BaseFinancialModel


# Сигнал, который вызывается перед удалением объекта BankAccount
@receiver(pre_delete, sender=BankAccount)
def bank_account_pre_delete(sender, instance, **kwargs):
    # Получаем все финансовые поля из модели BaseFinancialModel
    financial_fields = [
        field.name for field in BaseFinancialModel._meta.fields
    ]
    # Итерируем по всем финансовым полям
    for field in financial_fields:
        # Получаем текущее значение поля удаляемого объекта
        value = getattr(instance, field)
        # Вычитаем значение из соответствующего поля
        # у сгуппированного банковского аккаунта
        setattr(
            instance.joint_bank_account,
            field,
            getattr(instance.joint_bank_account, field) - value
        )

    # Сохраняем изменения в связанном банковском аккаунте
    instance.joint_bank_account.save(update_fields=[*financial_fields])

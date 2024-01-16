import re
from datetime import datetime

from .models import (
    BalanceSheet, FinancialClass,
    JointBankAccount, BankAccount, BaseFinancialModel
)

EXCEL_DATE_PATTERN = r'\b\d{2}\.\d{2}\.\d{4}\b'
FINANCIAL_FIELDS = BaseFinancialModel._meta.fields


def parse_excel_dates(date_str):
    matches = re.findall(EXCEL_DATE_PATTERN, date_str)
    start_period_str, end_period_str = matches
    start_period = datetime.strptime(start_period_str, '%d.%m.%Y')
    end_period = datetime.strptime(end_period_str, '%d.%m.%Y')
    return start_period, end_period


def create_or_update_balance_sheet(excel_file, bank, start_period, end_period):
    balance_sheet, _ = BalanceSheet.objects.get_or_create(
        start_period=start_period,
        end_period=end_period,
        bank=bank,
    )
    balance_sheet.file = excel_file
    balance_sheet.save(update_fields=['file'])
    return balance_sheet


def process_excel_row(
    cell_values, balance_sheet, current_joint_code, current_class
):
    if "КЛАСС" in str(cell_values[0]):
        current_class = process_class_row(cell_values[0], balance_sheet)
    elif is_valid_code(cell_values[0]):
        joint_code, code = str(cell_values[0])[:2], str(cell_values[0])
        if not current_joint_code or current_joint_code != joint_code:
            joint_bank_account, current_joint_code = (
                process_joint_bank_account(
                    joint_code, current_joint_code, current_class
                )
            )
        process_bank_account(cell_values, code, joint_bank_account)
    return current_class


def process_class_row(cell_value, balance_sheet):
    match = re.search(r'(\d+)\s+(.+)', str(cell_value))
    if match:
        number = int(match.group(1))
        name = match.group(2)
        current_class, _ = FinancialClass.objects.get_or_create(
            number=number,
            name=name,
            balance_sheet=balance_sheet
        )
        return current_class


def is_valid_code(cell_value):
    return (isinstance(cell_value, int) and 1000 <= cell_value <= 9999) or (
        (isinstance(cell_value, str) and len(cell_value) == 4 and (
            cell_value.isdigit()
        )))


def process_joint_bank_account(joint_code, current_joint_code, current_class):
    joint_bank_account, _ = JointBankAccount.objects.get_or_create(
        code=joint_code,
        financial_class=current_class
    )
    current_joint_code = joint_code
    return joint_bank_account, current_joint_code


def process_bank_account(cell_values, code, joint_bank_account):
    values_list = cell_values[1:5]
    bank_account_data = {
        field.name: value for field, value in zip(
            FINANCIAL_FIELDS, values_list
        )}
    print(code)
    BankAccount.objects.get_or_create(
        code=code,
        joint_bank_account=joint_bank_account,
        **bank_account_data
    )

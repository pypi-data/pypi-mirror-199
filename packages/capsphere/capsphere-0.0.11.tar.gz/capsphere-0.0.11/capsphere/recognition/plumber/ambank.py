import pdfplumber
from typing import Union
from decimal import Decimal
import pandas as pd
import numpy as np
import re

HEADERS = ['date', 'transaction', 'cheque_no',
           'debit', 'credit', 'balance']

TWO_PLACES = Decimal(10) ** -2


def convert_bytes_to_df(content: Union[bytes, str]) -> tuple:
    total_transactions = []
    pdf = pdfplumber.open(content)
    total_pages = len(pdf.pages)
    for index in range(total_pages):
        if __check_if_tables_found(pdf.pages[index]):
            page_table = pdf.pages[index].extract_table(table_settings={"vertical_strategy": "lines_strict"})
            for transaction in page_table:
                if __check_all_entries_empty(transaction):
                    break
                total_transactions.append(transaction)
    df = pd.DataFrame(total_transactions, columns=HEADERS)

    df = df.replace('', np.nan)
    transformed_df = df.groupby((~df['date'].isnull()).cumsum()).agg({'date': 'first',
                                                                      'transaction': lambda x: '\n'.join(x),
                                                                      'cheque_no': 'first',
                                                                      'debit': 'first',
                                                                      'credit': 'first',
                                                                      'balance': 'first'}).fillna('')
    transformed_df.index.name = None
    transformed_df['debit'] = __format_column(transformed_df['debit'])
    transformed_df['credit'] = __format_column(transformed_df['credit'])
    transformed_df['balance'] = __format_column(transformed_df['balance'])

    total_debit = pd.to_numeric(
        transformed_df['debit']).sum()
    total_credit = pd.to_numeric(
        transformed_df['credit']).sum()
    total_deb_transactions = df[df['debit'].notnull()].debit.size
    total_cred_transactions = df[df['credit'].notnull()].credit.size

    return Decimal(transformed_df['balance'].iloc[0]).quantize(TWO_PLACES), \
        Decimal(transformed_df['balance'].iloc[-1]).quantize(TWO_PLACES), \
        Decimal(total_debit).quantize(TWO_PLACES), \
        Decimal(total_credit).quantize(TWO_PLACES), \
        Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
        Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
        transformed_df['date'].iloc[-1]


def convert_month(date_range: str) -> str:
    pattern = r"(\b(0?[1-9]|[12]\d|3[01])\b)/(\b(0?[1-9]|1[0-2])\b)/(\d{4})"
    dates = re.findall(pattern, date_range)
    if dates:
        return [(t[0], t[2], t[4]) for t in dates]
    else:
        raise Exception(f"Unable to match date range {date_range}")


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def __check_all_entries_empty(transaction) -> bool:
    return True if all(entry == '' or entry.isspace() for entry in transaction) else False


def __format_column(df_column: pd.Series) -> pd.Series:
    return df_column.str.replace(',', '').replace('', '0.00')


def __check_if_tables_found(content) -> bool:
    check = content.find_tables(table_settings={"vertical_strategy": "lines_strict"})
    return True if len(check) > 0 else False

import pdfplumber
from typing import Union
from capsphere.common.utils import read_config


def extract_bank_name(file_path: Union[str, bytes]) -> str:

    # TODO Compare pdfplumber output and return the string of the bank in this function
    # TODO write a test in test_reader if possible
    extracted_bank_name = None
    pdf = pdfplumber.open(file_path)

    first_page = pdf.pages[0]
    first_page.to_image()

    if _search_for_text(first_page):
        extracted_bank_name = _search_for_text(first_page)
        return extracted_bank_name

    # check on last page if could not find anything on first page
    if extracted_bank_name is None:
        last_page = pdf.pages[-1]
        last_page.to_image()
        if _search_for_text(last_page):
            extracted_bank_name = _search_for_text(last_page)
            return extracted_bank_name
        else:
            return "Could not get the bank name"


def _search_for_text(image) -> str:
    bank_schemas = read_config()
    for bank in bank_schemas:
        for identifier in bank['identifiers']:
            if image.search(identifier, regex=True, case=False):
                return bank['name']

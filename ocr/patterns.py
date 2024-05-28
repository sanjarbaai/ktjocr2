import re

NUMBER_OF_CONTRACT_PATTERN = re.compile(r'\d{2}[А-ЯA-Z][А-ЯA-Z]-[А-ЯA-Z]-\d{4}')

DATE_PATTERN = re.compile(r'\b(?:\d{1,2}[.,]\d{1,2}[.,]\d{2,4}|\d{4}[.,]\d{2}[.,]\d{2})(?:,)?\b')

PACKAGE_LIST_PATTERN = re.compile(r'[A-Z]{3}-(?:[A-Z]{3}|\d{3}|\d[A-Z]{2}|\d[a-z]\d)')

DIGITS_PATTERN = re.compile(r"\d+")

WORD = re.compile(r"\w+")

LONG_INTEGER_PATTERN = re.compile(r"\b\d{11,}\b")

TERMS_OF_DELIVERY_PATTERN = re.compile(r'delivery:(.*)')
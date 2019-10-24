import logger
from schematics.models import Model
from schematics.types import URLType, StringType, ListType, DateTimeType
from schematics.exceptions import ValidationError
from scrapper.banks_data import country_name_iso, currency_name_iso
from iso4217 import Currency

my_logger = logger.get_logger("my_log")


def is_valid_country_iso(value):
    if not country_name_iso.__contains__(value):
        my_logger.error(f'Invalid country ISO code {value}')
        raise ValidationError(f'Invalid country ISO code {value}')
    return value


def is_valid_currency_iso(value):
    # if not currency_name_iso.__contains__(value):
    #     raise ValidationError(f'Invalid currency ISO code {value}')
    # return value
    try:
        Currency(value)
    except:
        my_logger.error(f'Invalid currency ISO code {value}')
        raise ValidationError(f'Invalid currency ISO code {value}')
    return value


class ItemValidator(Model):
    name = StringType()
    country = StringType(validators=[is_valid_country_iso])
    time = StringType()
    fromCurrency = ListType(StringType(validators=[is_valid_currency_iso]))
    toCurrency = ListType(StringType(validators=[is_valid_currency_iso]))
    buyMargin = ListType(StringType)
    sellMargin = ListType(StringType)
    unit = StringType()

import logger
from schematics.models import Model
from schematics.types import StringType, ListType, BooleanType, BaseType
from schematics.exceptions import ValidationError
from scrapper.iso_data import country_name_iso, currency_name_iso
from iso4217 import Currency

my_logger = logger.get_logger("my_log")


def is_valid_unit(value):
    valid_unit = ["M100", "M1000", "percentage", "exchange", "exchange100"]

    if not valid_unit.__contains__(value):
        my_logger.error(f'Invalid unit: {value}')
        raise ValidationError(f'Invalid unit: {value}')
    return value


def is_valid_margin(value):
    try:
        value = float(value)
        return str(value)
    except ValueError:
        raise ValidationError(f'Invalid margin: {value}')


def is_valid_country_iso(value):
    if not country_name_iso.__contains__(value):
        my_logger.error(f'Invalid country ISO code: {value}')
        raise ValidationError(f'Invalid country ISO code: {value}')
    return value


def is_valid_currency_iso(value):
    if not currency_name_iso.__contains__(value):
        my_logger.error(f'Invalid currency ISO code: {value}')
        raise ValidationError(f'Invalid currency ISO code {value}')
    return value
    # try:
    #     Currency(value)
    # except:
    #     my_logger.error(f'Invalid currency ISO code: {value}')
    #     raise ValidationError(f'Invalid currency ISO code: {value}')
    # return value


class ItemValidator(Model):
    name = StringType()
    country = StringType(validators=[is_valid_country_iso])
    time = StringType()
    fromCurrency = ListType(StringType(validators=[is_valid_currency_iso]))
    toCurrency = ListType(StringType(validators=[is_valid_currency_iso]))
    unit = StringType(validators=[is_valid_unit])
    buyMargin = ListType(StringType(validators=[is_valid_margin]))
    sellMargin = ListType(StringType(validators=[is_valid_margin]))
    isCrossInverted = BooleanType()
    exchangeUnit = BaseType()

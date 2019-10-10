from schematics.models import Model
from schematics.types import URLType, StringType, ListType


class ItemValidator(Model):
    print("__________Validator class")
    to_currency = ListType(StringType(required=True))
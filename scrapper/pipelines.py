from __future__ import absolute_import
import six
import json
import smtplib, ssl
from io import BytesIO
from collections import defaultdict
from scrapy.exceptions import DropItem, NotConfigured
from scrapy.utils.misc import load_object
from scrapy.exporters import JsonLinesItemExporter
from scrapy import Field, Item
from scrapy.utils.python import to_native_str
from spidermon.contrib.validation import SchematicsValidator, JSONSchemaValidator
from spidermon.contrib.validation.jsonschema.tools import get_schema_from
from schematics.models import Model
from spidermon.contrib.scrapy.stats import ValidationStatsManager
import requests
from environment import environment
from scrapper.settings import ERROR_EMAIL_PORT, ERROR_EMAIL_SMTP_SERVER, ERROR_EMAIL_SENDER
from scrapper.settings import ERROR_EMAIL_RECEIVER, ERROR_EMAIL_PASSWORD


class DisplayItem(object):
    def process_item(self, item, spider):

        the_longest = max(len(item['toCurrency']), max(len(item['sellMargin']), len(item['buyMargin'])))

        print(f'PARSED---------{item["name"]}------------')
        for i in range(the_longest):

            string = f"{i}.\t{item['fromCurrency']}"
            if len(item['toCurrency']) > i:
                string += f"\t\t{item['toCurrency'][i]}"
            if len(item['sellMargin']) > i:
                string += f"\t\t{item['sellMargin'][i]}"
            if len(item['buyMargin']) > i:
                string += f"\t\t{item['buyMargin'][i]}"
            if len(item['exchangeUnit']) > i and item['exchangeUnit'] != '':
                string += f"\t\t{item['exchangeUnit'][i]}"

            print(string)
        return item


class DropEmptyRows(object):
    def process_item(self, item, spider):
        the_longest = max(len(item['toCurrency']), max(len(item['sellMargin']), len(item['buyMargin'])))

        temp_to_currency = []
        temp_buy_margin = []
        temp_sell_margin = []

        for i in range(the_longest):
            if len(item['toCurrency']) > i and len(item['sellMargin']) > i and len(item['buyMargin']) > i:
                if item['toCurrency'][i] == '' and item['sellMargin'][i] == '' and item['buyMargin'][i] == '':
                    pass
                else:
                    temp_to_currency.append(item['toCurrency'][i])
                    temp_sell_margin.append(item['sellMargin'][i])
                    temp_buy_margin.append(item['buyMargin'][i])
            else:
                if len(item['toCurrency']) > i:
                    temp_to_currency.append(item['toCurrency'][i])
                if len(item['sellMargin']) > i:
                    temp_sell_margin.append(item['sellMargin'][i])
                if len(item['buyMargin']) > i:
                    temp_buy_margin.append(item['buyMargin'][i])

        item['toCurrency'] = temp_to_currency
        item['sellMargin'] = temp_sell_margin
        item['buyMargin'] = temp_buy_margin
        return item


class LevelColumns(object):
    def process_item(self, item, spider):
        the_longest = max(len(item['toCurrency']), max(len(item['sellMargin']), len(item['buyMargin'])))

        temp_to_currency = []
        temp_buy_margin = []
        temp_sell_margin = []

        if len(item['toCurrency']) == len(item['sellMargin']) == len(item['buyMargin']):
            for i in range(the_longest):
                temp_to_currency.append('-' if item['toCurrency'][i] == '' else item['toCurrency'][i])
                temp_sell_margin.append('-' if item['sellMargin'][i] == '' else item['sellMargin'][i])
                temp_buy_margin.append('-' if item['buyMargin'][i] == '' else item['buyMargin'][i])
        else:
            for i in range(the_longest):
                if len(item['toCurrency']) > i and item['toCurrency'][i] != '':
                    temp_to_currency.append(item['toCurrency'][i])
                if len(item['sellMargin']) > i and item['sellMargin'][i] != '':
                    temp_sell_margin.append(item['sellMargin'][i])
                if len(item['buyMargin']) > i and item['buyMargin'][i] != '':
                    temp_buy_margin.append(item['buyMargin'][i])

        item['toCurrency'] = temp_to_currency
        item['sellMargin'] = temp_sell_margin
        item['buyMargin'] = temp_buy_margin

        return item


class DropRowsWithNoMargin(object):
    def process_item(self, item, spider):
        the_longest = max(len(item['toCurrency']), max(len(item['sellMargin']), len(item['buyMargin'])))

        temp_to_currency = []
        temp_buy_margin = []
        temp_sell_margin = []

        for i in range(the_longest):
            condition_one = item['toCurrency'][i] != '' and item['sellMargin'][i] != '-' and item['buyMargin'][i] == '-'
            condition_two = item['toCurrency'][i] != '' and item['sellMargin'][i] == '-' and item['buyMargin'][i] != '-'
            condition_three = item['toCurrency'][i] != '' and item['sellMargin'][i] == '-' and item['buyMargin'][
                i] == '-'

            if condition_one or condition_two or condition_three:
                pass
            else:
                temp_to_currency.append(item['toCurrency'][i])
                temp_sell_margin.append(item['sellMargin'][i])
                temp_buy_margin.append(item['buyMargin'][i])

        item['toCurrency'] = temp_to_currency
        item['sellMargin'] = temp_sell_margin
        item['buyMargin'] = temp_buy_margin
        return item


class CalculateExchangePerOneUnit(object):
    def process_item(self, item, spider):  # this method is prepared for sending data to "margin saver"
        if len(item['exchangeUnit']) > 1:
            the_longest = max(len(item['sellMargin']), len(item['buyMargin']))

            temp_buy_margin = []
            temp_sell_margin = []

            for i in range(the_longest):
                temp_sell_margin.append(str(round(float(item['sellMargin'][i]) / float(item['exchangeUnit'][i]), 4)))
                temp_buy_margin.append(str(round(float(item['buyMargin'][i]) / float(item['exchangeUnit'][i]), 4)))

            item['sellMargin'] = temp_sell_margin
            item['buyMargin'] = temp_buy_margin
        return item


class SendData(object):
    def process_item(self, item, spider):  # this method is prepared for sending data to "margin saver"
        item['fromCurrency'] = item['fromCurrency'] * len(item['toCurrency'])  # to fill the from currency column

        url = environment.margin_saver_service_url() + "/margin"

        results = dict(item)
        del results['exchangeUnit']
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post(url, data=json.dumps(results), headers=headers)
        return item


# --------------------------- MODIFIED -------------------------------------------------
# 'spidermon.contrib.scrapy.pipelines.ItemValidationPipeline'
# to send more meaningful email notifications while there is an validation error
# --------------------------------------------------------------------------------------
DEFAULT_ERRORS_FIELD = "_validation"
DEFAULT_ADD_ERRORS_TO_ITEM = False
DEFAULT_DROP_ITEMS_WITH_ERRORS = False


class ItemValidationPipeline(object):
    def __init__(
            self,
            validators,
            stats,
            drop_items_with_errors=DEFAULT_DROP_ITEMS_WITH_ERRORS,
            add_errors_to_items=DEFAULT_ADD_ERRORS_TO_ITEM,
            errors_field=None,
    ):
        self.drop_items_with_errors = drop_items_with_errors
        self.add_errors_to_items = add_errors_to_items or DEFAULT_ADD_ERRORS_TO_ITEM
        self.errors_field = errors_field or DEFAULT_ERRORS_FIELD
        self.validators = validators
        self.stats = ValidationStatsManager(stats)
        for _type, vals in validators.items():
            [self.stats.add_validator(_type, val.name) for val in vals]

    @classmethod
    def from_crawler(cls, crawler):
        validators = defaultdict(list)
        allowed_types = (list, tuple, dict)

        def set_validators(loader, schema):
            if type(schema) in (list, tuple):
                schema = {Item: schema}
            for obj, paths in schema.items():
                key = obj.__name__
                paths = paths if type(paths) in (list, tuple) else [paths]
                objects = [loader(v) for v in paths]
                validators[key].extend(objects)

        for loader, name in [
            (cls._load_jsonschema_validator, "SPIDERMON_VALIDATION_SCHEMAS"),
            (cls._load_schematics_validator, "SPIDERMON_VALIDATION_MODELS"),
        ]:
            res = crawler.settings.get(name)
            if not res:
                continue
            if type(res) not in allowed_types:
                raise NotConfigured(
                    "Invalid <{}> type for <{}> settings, dict or list/tuple"
                    "is required".format(type(res), name)
                )
            set_validators(loader, res)

        if not validators:
            raise NotConfigured("No validators were found")

        return cls(
            validators=validators,
            stats=crawler.stats,
            drop_items_with_errors=crawler.settings.getbool(
                "SPIDERMON_VALIDATION_DROP_ITEMS_WITH_ERRORS"
            ),
            add_errors_to_items=crawler.settings.getbool(
                "SPIDERMON_VALIDATION_ADD_ERRORS_TO_ITEMS"
            ),
            errors_field=crawler.settings.get("SPIDERMON_VALIDATION_ERRORS_FIELD"),
        )

    @classmethod
    def _load_jsonschema_validator(cls, schema):
        if isinstance(schema, six.string_types):
            schema = get_schema_from(schema)
        if not isinstance(schema, dict):
            raise NotConfigured(
                "Invalid schema, jsonschemas must be defined as:\n"
                "- a python dict.\n"
                "- an object path to a python dict.\n"
                "- an object path to a JSON string.\n"
                "- a path to a JSON file."
            )
        return JSONSchemaValidator(schema)

    @classmethod
    def _load_schematics_validator(cls, model_path):
        model_class = load_object(model_path)
        if not issubclass(model_class, Model):
            raise NotConfigured(
                "Invalid model, models must subclass schematics.models.Model"
            )
        return SchematicsValidator(model_class)

    def process_item(self, item, _):
        validators = self.find_validators(item)
        if not validators:
            # No validators match this specific item type
            return item

        data = self._convert_item_to_dict(item)
        self.stats.add_item()
        self.stats.add_fields(len(list(data.keys())))
        for validator in validators:
            ok, errors = validator.validate(data)
            if not ok:
                self.send_mail(item, errors)
                self._add_error_stats(errors)
                if self.add_errors_to_items:
                    self._add_errors_to_item(item, errors)
                if self.drop_items_with_errors:
                    self._drop_item(item, errors)
        return item

    # TODO: make general method/class to send alerts (similar method in "quote_spider.py")
    def send_mail(self, item, errors):

        message = f"""\
        Subject: Scraper error logs

        Bank: {item['name']} \n
        Errors: {errors}
        """
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(ERROR_EMAIL_SMTP_SERVER, ERROR_EMAIL_PORT, context=context) as server:
            server.login(ERROR_EMAIL_SENDER, ERROR_EMAIL_PASSWORD)
            server.sendmail(ERROR_EMAIL_SENDER, ERROR_EMAIL_RECEIVER, message)

    def find_validators(self, item):
        find = lambda x: self.validators.get(x.__name__, [])
        return find(item.__class__) or find(Item)

    def _convert_item_to_dict(self, item):
        serialized_json = BytesIO()
        exporter = JsonLinesItemExporter(serialized_json)
        exporter.export_item(item)
        data = json.loads(to_native_str(serialized_json.getvalue(), exporter.encoding))
        serialized_json.close()
        return data

    def _add_errors_to_item(self, item, errors):
        try:
            if self.errors_field not in item.__class__.fields:
                item.__class__.fields[self.errors_field] = Field()
            if self.errors_field not in item._values:
                item[self.errors_field] = defaultdict(list)
        except AttributeError:
            # The item is just a dict object instead of a Scrapy.Item object
            if self.errors_field not in item:
                item[self.errors_field] = defaultdict(list)
        for field_name, messages in errors.items():
            item[self.errors_field][field_name] += messages

    def _drop_item(self, item, errors):
        """
        This method drops the item after detecting validation errors. Note
        that you could override it to add more details about the item that
        is being dropped or to drop the item only when some specific errors
        are detected.
        """
        self.stats.add_dropped_item()
        raise DropItem("Validation failed!")

    def _add_error_stats(self, errors):
        """
        This method adds validation error stats that can be later used to
        detect alert conditions in the monitors.
        """
        for field_name, messages in errors.items():
            for message in messages:
                self.stats.add_field_error(field_name, message)
        self.stats.add_item_with_errors()

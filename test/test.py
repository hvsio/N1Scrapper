import unittest
from scrapper.iso_data import country_name_iso
from scrapper import validators


class TestMethods(unittest.TestCase):

    def test_is_unit_valid_caseValid(self):
        valid_units = ["M100", "M1000", "percentage", "exchange"]
        for value in valid_units:
            self.assertEqual(validators.is_valid_unit(value), value)

    def test_is_unit_valid_caseInValid(self):
        invalid_units = ['M10', None, '%', 'unit', '&^%$', 54, 'abc']
        for value in invalid_units:
            self.assertRaises(validators.ValidationError, validators.is_valid_unit, value)

    def test_is_country_code_valid_caseValid(self):
        for value in country_name_iso.keys():
            self.assertEqual(validators.is_valid_country_iso(value), value)

    def test_is_country_code_valid_caseInValid(self):
        invalid_country = ["M100", None, 56, "!@#", "Poland"]
        for value in invalid_country:
            self.assertRaises(validators.ValidationError, validators.is_valid_country_iso, value)

    def test_is_currency_code_valid_caseValid(self):
        value = 'EUR'
        self.assertEqual(validators.is_valid_currency_iso(value), value)

    def test_is_currency_code_valid_caseInValid(self):
        invalid_currency = ["Euro", None, 56, "!@#", "eur"]
        for value in invalid_currency:
            self.assertRaises(validators.ValidationError, validators.is_valid_currency_iso, value)


if __name__ == '__main__':
    unittest.main()

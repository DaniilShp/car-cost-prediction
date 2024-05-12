import json
import unittest

from bs4 import BeautifulSoup
from .. import drom_parser


class TestDromParser(unittest.TestCase):

    def test_get_html_with_correct_url(self):
        correct_url = "https://auto.drom.ru/audi/"
        parser = drom_parser.DromParser(url_to_parse=correct_url)
        self.assertEqual(parser.page.status_code, 200)

    def test_get_html_with_blocked_url(self):
        blocked_url = "https://www.avito.ru/"
        with self.assertRaises(ValueError):
            parser = drom_parser.DromParser(url_to_parse=blocked_url)
            self.assertEqual(parser.page.status_code, 403)

    def test_parsing(self):
        filename = "audi_a4"
        parser = drom_parser.DromParser("https://auto.drom.ru/")
        with open(f"parsing/tests/test_html/{filename}.html", "r") as f:
            parser.page = f.read()
            parser.soup = BeautifulSoup(parser.page, "html.parser")
        parser.parse()
        with open(f"parsing/tests/json_answer/{filename}.json", 'r') as file:
            deserialized_result = json.load(file)
        self.assertEqual(parser.resulting_dicts, deserialized_result)


if __name__ == '__main__':
    unittest.main()

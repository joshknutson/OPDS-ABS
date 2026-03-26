import unittest

from lxml import etree

from opds_abs.utils.xml_utils import dict_to_xml


class TestDictToXml(unittest.TestCase):
    def test_basic_dict_to_xml(self):
        root = etree.Element("root")
        dict_to_xml(root, {
            "title": {"_text": "Hello World"},
            "link": {"_attrs": {"href": "http://example.com", "rel": "self"}},
        })

        title_el = root.find("title")
        self.assertIsNotNone(title_el)
        self.assertEqual(title_el.text, "Hello World")

        link_el = root.find("link")
        self.assertIsNotNone(link_el)
        self.assertEqual(link_el.get("href"), "http://example.com")
        self.assertEqual(link_el.get("rel"), "self")

    def test_list_items_become_multiple_elements(self):
        root = etree.Element("root")
        dict_to_xml(root, {
            "link": [
                {"_attrs": {"href": "http://example.com/1"}},
                {"_attrs": {"href": "http://example.com/2"}},
            ]
        })

        links = root.findall("link")
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0].get("href"), "http://example.com/1")
        self.assertEqual(links[1].get("href"), "http://example.com/2")

import unittest

import wikitextparser as wtp

import mediawiki.mediawiki_parse as mp

class TestMediawikiCreate(unittest.TestCase):
    def test_read_wikilink_masked(self):
        wikilink_text = "[[User:tarsa129|the best modder]]"
        wikilink = wtp.parse(wikilink_text)
        actual_title, actual_text = mp.read_wikilink(wikilink.wikilinks[0])
        self.assertEqual(actual_title, "User:tarsa129")
        self.assertEqual(actual_text, "the best modder")

    def test_read_wikilink_notmasked(self):
        wikilink_text = "[[User:tarsa129]]"
        wikilink = wtp.parse(wikilink_text)
        actual_title, actual_text = mp.read_wikilink(wikilink.wikilinks[0])
        self.assertEqual(actual_title, "User:tarsa129")
        self.assertEqual(actual_text, "User:tarsa129")

    def test_read_template_empty(self):
        template_text = """{{Template Name}}}"""
        actual_template = mp.read_template(template_text)
        self.assertDictEqual({}, actual_template)

    def test_read_template_oneline(self):
        template_text = """{{Template Name|Param 1}}}"""
        actual_template = mp.read_template(template_text)
        self.assertDictEqual({"1":"Param 1"}, actual_template)

    def test_read_template_multiline(self):
        template_text = """{{Template Name
|Arg 1= Value 1
|Arg 2= Value 2
}}"""
        expected_template = {"Arg 1": 'Value 1', "Arg 2": "Value 2"}
        actual_template = mp.read_template(template_text)
        self.assertDictEqual(expected_template, actual_template)

    def test_read_template_multiline_reparsed(self):
            template_text = """{{Template Name
    |Arg 1= Value 1
    |Arg 2= Value 2
    }}"""
            template_parsed = wtp.parse(template_text)
            expected_template = {"Arg 1": 'Value 1', "Arg 2": "Value 2"}
            actual_template = mp.read_template(template_parsed)
            self.assertDictEqual(expected_template, actual_template)

    def test_read_template_notemplate(self):
        template_text = "[[Wikilink]]"
        self.assertRaises(RuntimeError, mp.read_template, template_text)

    def test_read_table_topcaption(self):
        table_text = """{|
|+ Header
! Author
! Track
|- 
| [[tarsa129]] || not Toad's temple
|- 
| [[LucioWins]]
| Toad's Temple
|}"""
        expected_data = [{"Author":"[[tarsa129]]", "Track":"not Toad's temple"},
                         {"Author": "[[LucioWins]]", "Track": "Toad's Temple"}]
        actual_data = mp.read_table_topcaption(table_text)
        self.assertDictEqual(expected_data[0], actual_data[0])
        self.assertDictEqual(expected_data[1], actual_data[1])

    def test_read_table_topcaption_notable(self):
        self.assertRaises(RuntimeError, mp.read_table_topcaption, "")

    def test_read_table_sidecaption(self):
        table_text = """{|
|+ Header
! Author:
| [[tarsa129]]
|-
! Cover:
| [[File:Indexkartdiddy.png]]
|}"""
        expected_data = {"name":"Header", "Author:":["[[tarsa129]]"], "Cover:":["[[File:Indexkartdiddy.png]]"]}
        actual_data = mp.read_table_sidecaption(table_text)
        self.assertDictEqual(expected_data, actual_data)


    def test_read_table_sidecaption_notable(self):
        self.assertRaises(RuntimeError, mp.read_table_sidecaption, "")

if __name__ == '__main__':
    unittest.main()

import unittest

import mediawiki.mediawiki_create as mc

class TestMediawikiCreate(unittest.TestCase):
    def test_create_template_from_args(self):
        template_arguments = {"Arg 1":'Value 1', "Arg 2":"Value 2"}
        template_name = "Template Name"
        expected_text = """{{Template Name
|Arg 1= Value 1
|Arg 2= Value 2
}}"""
        actual_text = mc.create_template_from_args(template_arguments, template_name)
        self.assertEqual(expected_text, actual_text)  # add assertion here


if __name__ == '__main__':
    unittest.main()

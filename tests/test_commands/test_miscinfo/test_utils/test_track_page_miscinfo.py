import unittest

from commands.miscinfo.utils import track_page_miscinfo as tpm

class TextTrackPageMiscinfo(unittest.TestCase):
    def test_get_miscinfo_template(self):
        page_text = "{{Misc-Info\n|name= {{PAGENAME}}\n|download = link}}"
        actual_dict = tpm.get_miscinfo_template(page_text)
        expected_dict = tpm.get_ordered_miscinfo_arguments() | {"name": "{{PAGENAME}}", "download": "link"}
        self.assertDictEqual(actual_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()

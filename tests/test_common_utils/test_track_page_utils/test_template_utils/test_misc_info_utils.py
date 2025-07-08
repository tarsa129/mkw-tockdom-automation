import unittest

from common_utils.track_page_utils.template_utils import misc_info_utils as miu

class TextTrackPageMiscinfo(unittest.TestCase):
    def test_get_miscinfo_template(self):
        page_text = "{{Misc-Info\n|name= {{PAGENAME}}\n|download = link}}"
        actual_dict = miu.get_miscinfo_template(page_text)
        expected_dict = miu.get_ordered_miscinfo_arguments() | {"name": "{{PAGENAME}}", "download": "link"}
        self.assertDictEqual(actual_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()

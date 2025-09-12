import unittest
import warnings

import commands.distro_list.utils.distro_section_contents as dsc
import wikitextparser as wtp


class TestTrackPageHandler(unittest.TestCase):
    def test_fix_distro_custom_name(self):
        orig_name = "Tarsa's Epic Track Pack"
        new_name = dsc.fix_distro_custom_name(orig_name)
        self.assertEqual(orig_name, new_name)

    def test_fix_distro_custom_name_the(self):
        orig_name = "The Tarsa's Epic Track Pack"
        new_name = dsc.fix_distro_custom_name(orig_name)
        self.assertEqual(new_name, "Tarsa's Epic Track Pack")

    def test_fix_distro_custom_name_all_lower(self):
        orig_name = "debut pack"
        new_name = dsc.fix_distro_custom_name(orig_name)
        self.assertEqual(orig_name, new_name)

    def test_fix_distro_custom_name_all_upper_later(self):
        orig_name = "debut Pack"
        new_name = dsc.fix_distro_custom_name(orig_name)
        self.assertEqual("Pack", new_name)

    def test_fix_distro_custom_name_number(self):
        orig_name = "0 debut Pack"
        new_name = dsc.fix_distro_custom_name(orig_name)
        self.assertEqual(orig_name, new_name)

    def test_read_distro_name_wiikilink(self):
        actual_distro_name = "Distro Name"
        distro_text = f"[[{actual_distro_name}]]"
        distro_name = dsc.read_distro_name(distro_text)
        self.assertEqual(distro_name, actual_distro_name)

    def test_read_distro_name_wiikilink_plus(self):
        actual_distro_name = "Distro Name"
        distro_text = f"[[{actual_distro_name}]] (v2.0)"
        distro_name = dsc.read_distro_name(distro_text)
        self.assertEqual(distro_name, actual_distro_name)

    def test_read_distro_name_template(self):
        actual_distro_name = "Distro Name"
        distro_text = f"{{{{Distrib-ref|{actual_distro_name}|129129|tarsa-pack}}}}"
        distro_name = dsc.read_distro_name(distro_text)
        self.assertEqual(distro_name, actual_distro_name)

    def test_read_distro_name_template_invalid(self):
        actual_distro_name = "Distro Name"
        distro_text = f"{{{{Distrib-ref|{actual_distro_name}|129129}}}}"
        self.assertRaises(AssertionError, dsc.read_distro_name, distro_text)

        distro_text = f"{{{{Distrib-Ref|{actual_distro_name}|129129|tarsa-pack}}}}"
        self.assertRaises(AssertionError, dsc.read_distro_name, distro_text)

    def test_read_distro_name_none(self):
        distro_text = " (none)"
        self.assertIsNone(dsc.read_distro_name(distro_text))

    def test_read_distro_name_other(self):
        distro_text = "Distro"
        self.assertEqual(dsc.read_distro_name(distro_text), distro_text)

    def test_get_distros_from_section(self):
        section_text = """This track is part of the following [[Custom Track Distribution]]s:
* [[Distro Name 1]]
* {{Distrib-ref|Distro Name 2|123123|distro-name}}
{{User-tarsa129-Link}}
[[Category:Track/Custon]]
"""
        expected_distros = {
            "Distro Name 1": "[[Distro Name 1]]",
            "Distro Name 2": "{{Distrib-ref|Distro Name 2|123123|distro-name}}"
        }
        distros = dsc.get_distros_from_section(wtp.parse(section_text))

        self.assertDictEqual(distros, expected_distros)

    def test_get_distros_from_section_empty(self):
        section_text = """This track is part of the following [[Custom Track Distribution]]s:
* (none)
"""
        expected_distros = {}
        with warnings.catch_warnings(record=True) as w:
            distros = dsc.get_distros_from_section(wtp.parse(section_text))
            self.assertDictEqual(distros, expected_distros)
            self.assertEqual(len(w), 1)


    def test_get_distros_from_section_invalid(self):
        section_text = """This track is part of the following [[Custom Track Distribution]]s:
* {{Distrib-Ref|Distro Name 1|123123|distro-name}}
* {{Distrib-ref|Distro Name 2|distro-name}}"""

        self.assertRaises(AssertionError, dsc.get_distros_from_section, wtp.parse(section_text))

    def test_create_distros_list(self):
        distros = {
            "A Distro": "[[A Distro]]",
            "x Distro": "{{Distrib-ref|X Distro|129129|x-pack}}",
            "Y Distro": "[[Y Distro]] (v1.1)"
        }

        expected_text = "* [[A Distro]]\n* {{Distrib-ref|X Distro|129129|x-pack}}\n* [[Y Distro]] (v1.1)\n"
        actual_text = dsc.create_distros_list(distros)
        self.assertEqual(actual_text, expected_text)

    def test_create_distros_list_empty(self):
        distros = {}
        expected_text = "* (none)\n"
        actual_text = dsc.create_distros_list(distros)
        self.assertEqual(actual_text, expected_text)
import unittest
import unittest.mock as mock
import warnings

import commands.distro_list.utils.track_page_distros as tpd
import wikitextparser as wtp

class TestTrackPageHandler(unittest.TestCase):
    def test_fix_distro_custom_name(self):
        orig_name = "Tarsa's Epic Track Pack"
        new_name = tpd.fix_distro_custom_name(orig_name)
        self.assertEqual(orig_name, new_name)

    def test_fix_distro_custom_name_the(self):
        orig_name = "The Tarsa's Epic Track Pack"
        new_name = tpd.fix_distro_custom_name(orig_name)
        self.assertEqual(new_name, "Tarsa's Epic Track Pack")

    def test_fix_distro_custom_name_all_lower(self):
        orig_name = "debut pack"
        new_name = tpd.fix_distro_custom_name(orig_name)
        self.assertEqual(orig_name, new_name)

    def test_fix_distro_custom_name_all_upper_later(self):
        orig_name = "debut Pack"
        new_name = tpd.fix_distro_custom_name(orig_name)
        self.assertEqual("Pack", new_name)

    def test_fix_distro_custom_name_number(self):
        orig_name = "0 debut Pack"
        new_name = tpd.fix_distro_custom_name(orig_name)
        self.assertEqual(orig_name, new_name)

    def test_read_distro_name_wiikilink(self):
        actual_distro_name = "Distro Name"
        distro_text = f"[[{actual_distro_name}]]"
        distro_name = tpd.read_distro_name(distro_text)
        self.assertEqual(distro_name, actual_distro_name)

    def test_read_distro_name_wiikilink_plus(self):
        actual_distro_name = "Distro Name"
        distro_text = f"[[{actual_distro_name}]] (v2.0)"
        distro_name = tpd.read_distro_name(distro_text)
        self.assertEqual(distro_name, actual_distro_name)

    def test_read_distro_name_template(self):
        actual_distro_name = "Distro Name"
        distro_text = f"{{{{Distrib-ref|{actual_distro_name}|129129|tarsa-pack}}}}"
        distro_name = tpd.read_distro_name(distro_text)
        self.assertEqual(distro_name, actual_distro_name)

    def test_read_distro_name_template_invalid(self):
        actual_distro_name = "Distro Name"
        distro_text = f"{{{{Distrib-ref|{actual_distro_name}|129129}}}}"
        self.assertRaises(AssertionError, tpd.read_distro_name, distro_text)

        distro_text = f"{{{{Distrib-Ref|{actual_distro_name}|129129|tarsa-pack}}}}"
        self.assertRaises(AssertionError, tpd.read_distro_name, distro_text)

    def test_read_distro_name_none(self):
        distro_text = " (none)"
        self.assertIsNone(tpd.read_distro_name(distro_text))

    def test_read_distro_name_other(self):
        distro_text = "Distro"
        self.assertEqual(tpd.read_distro_name(distro_text), distro_text)

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
        distros = tpd.get_distros_from_section(wtp.parse(section_text))

        self.assertDictEqual(distros, expected_distros)

    def test_get_distros_from_section_empty(self):
        section_text = """This track is part of the following [[Custom Track Distribution]]s:
* (none)
"""
        expected_distros = {}
        with warnings.catch_warnings(record=True) as w:
            distros = tpd.get_distros_from_section(wtp.parse(section_text))
            self.assertDictEqual(distros, expected_distros)
            self.assertEqual(len(w), 1)


    def test_get_distros_from_section_invalid(self):
        section_text = """This track is part of the following [[Custom Track Distribution]]s:
* {{Distrib-Ref|Distro Name 1|123123|distro-name}}
* {{Distrib-ref|Distro Name 2|distro-name}}"""

        self.assertRaises(AssertionError, tpd.get_distros_from_section, wtp.parse(section_text))

    @mock.patch("commands.distro_list.utils.track_page_distros.get_section_from_page")
    def test_get_distrosection_from_page_fromtext(self, mock_read_text):
        distro_section_text = """== <span id=distrib-list>Custom Track Distributions</span> ==
This track is part of the following [[Custom Track Distribution]]s:
* {{Distrib-ref|Distro Name 1|123123|distro-name}}
* {{Distrib-ref|Distro Name 2|12|distro-name}}\n"""
        page_text = "Section that doesn't matter\n" + distro_section_text + """== Section ==\nMore stuff that does not matter"""
        mock_read_text.return_value = wtp.parse(distro_section_text)
        distro_section = tpd.get_distrosection_from_page(page_text)
        mock_read_text.assert_called_once()

        self.assertEqual(distro_section.string, distro_section_text)

    @mock.patch("commands.distro_list.utils.track_page_distros.read_text")
    def test_get_distrosection_from_page_fromtext_nosection(self, mock_read_text):
        page_text = "Has no sections"
        mock_read_text.return_value = wtp.parse(page_text)

        self.assertRaises(RuntimeError, tpd.get_distrosection_from_page, wtp.parse(page_text))
        mock_read_text.assert_not_called()

    def test_create_distros_list(self):
        distros = {
            "A Distro": "[[A Distro]]",
            "x Distro": "{{Distrib-ref|X Distro|129129|x-pack}}",
            "Y Distro": "[[Y Distro]] (v1.1)"
        }

        expected_text = "* [[A Distro]]\n* {{Distrib-ref|X Distro|129129|x-pack}}\n* [[Y Distro]] (v1.1)\n"
        actual_text = tpd.create_distros_list(distros)
        self.assertEqual(actual_text, expected_text)

    def test_create_distros_list_empty(self):
        distros = {}
        expected_text = "* (none)\n"
        actual_text = tpd.create_distros_list(distros)
        self.assertEqual(actual_text, expected_text)

    @mock.patch("commands.distro_list.utils.track_page_distros.read_text")
    def test_get_distros_sectionid_first(self, mock_read_text):
        page_text = """\n== <span id=distrib-list>Custom Track Distributions</span> ==
This track is part of the following [[Custom Track Distribution]]s:
* {{Distrib-ref|Distro Name 1|123123|distro-name}}
* {{Distrib-ref|Distro Name 2|12|distro-name}}\n"""
        mock_read_text.return_value = wtp.parse(page_text)
        distro_section_id = tpd.get_distros_sectionid(page_text)
        mock_read_text.assert_called_once()

        self.assertEqual(distro_section_id, 1)

    def test_get_distros_sectionid_middle_header(self):
        page_text = """first filler text== first section ==
filler text
== <span id=distrib-list>Custom Track Distributions</span> ==
This track is part of the following [[Custom Track Distribution]]s:
* {{Distrib-ref|Distro Name 1|123123|distro-name}}
* {{Distrib-ref|Distro Name 2|12|distro-name}}
=== inner section ===
more filler text"""
        distro_section_id = tpd.get_distros_sectionid(wtp.parse(page_text))

        self.assertEqual(distro_section_id, 1)

    def test_get_distros_sectionid_middle(self):
        page_text = """== first section ==
filler text
=== inner first section ===
filllller
== <span id=distrib-list>Custom Track Distributions</span> ==
This track is part of the following [[Custom Track Distribution]]s:
* {{Distrib-ref|Distro Name 1|123123|distro-name}}
* {{Distrib-ref|Distro Name 2|12|distro-name}}
=== inner section ===
more filler text"""
        distro_section_id = tpd.get_distros_sectionid(wtp.parse(page_text))

        self.assertEqual(distro_section_id, 3)

    def test_get_distros_sectionid_end(self):
        page_text = """== first section ==
filler text
== <span id=distrib-list>Custom Track Distributions</span> ==
This track is part of the following [[Custom Track Distribution]]s:
* {{Distrib-ref|Distro Name 1|123123|distro-name}}
* {{Distrib-ref|Distro Name 2|12|distro-name}}\n"""
        distro_section_id = tpd.get_distros_sectionid(wtp.parse(page_text))

        self.assertEqual(distro_section_id, 2)

    def test_get_distros_sectionid_none(self):
        page_text = """== first section ==\nfiller text\n"""
        distro_section_id = tpd.get_distros_sectionid(wtp.parse(page_text))

        self.assertEqual(distro_section_id, -1)
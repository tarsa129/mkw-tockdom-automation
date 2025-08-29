import unittest

import commands.distro_list.utils.distro_section_meta as dsm
import wikitextparser as wtp

class TestTrackPageHandler(unittest.TestCase):
    def test_get_distrosection_from_page_fromtext(self):
        distro_section_text = """== <span id=distrib-list>Custom Track Distributions</span> ==
    This track is part of the following [[Custom Track Distribution]]s:
    * {{Distrib-ref|Distro Name 1|123123|distro-name}}
    * {{Distrib-ref|Distro Name 2|12|distro-name}}\n"""
        page_text = "Section that doesn't matter\n" + distro_section_text + """== Section ==\nMore stuff that does not matter"""
        distro_section = dsm.get_distrosection_from_page(page_text)

        self.assertEqual(distro_section.string, distro_section_text)

    def test_get_distrosection_from_page_fromtext_nosection(self):
        page_text = "Has no sections"
        self.assertEqual(
            dsm.get_distrosectioninfo_from_page(wtp.parse(page_text)),
            (-1, None))

    def test_get_distros_sectionid_first(self):
        page_text = """\n== <span id=distrib-list>Custom Track Distributions</span> ==
This track is part of the following [[Custom Track Distribution]]s:
* {{Distrib-ref|Distro Name 1|123123|distro-name}}
* {{Distrib-ref|Distro Name 2|12|distro-name}}\n"""
        distro_section_id = dsm.get_distros_sectionid(page_text)

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
        distro_section_id = dsm.get_distros_sectionid(wtp.parse(page_text))

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
        distro_section_id = dsm.get_distros_sectionid(wtp.parse(page_text))

        self.assertEqual(distro_section_id, 3)

    def test_get_distros_sectionid_end(self):
        page_text = """== first section ==
filler text
== <span id=distrib-list>Custom Track Distributions</span> ==
This track is part of the following [[Custom Track Distribution]]s:
* {{Distrib-ref|Distro Name 1|123123|distro-name}}
* {{Distrib-ref|Distro Name 2|12|distro-name}}\n"""
        distro_section_id = dsm.get_distros_sectionid(wtp.parse(page_text))

        self.assertEqual(distro_section_id, 2)

    def test_get_distros_sectionid_none(self):
        page_text = """== first section ==\nfiller text\n"""
        actual_section_id = dsm.get_distros_sectionid(wtp.parse(page_text))
        self.assertEqual(actual_section_id, -1)
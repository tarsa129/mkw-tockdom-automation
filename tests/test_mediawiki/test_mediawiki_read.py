import unittest

from mediawiki import mediawiki_read as mr

class TestMediawikiRead(unittest.TestCase):
    def setUp(self):
        self.page_text = """== Section 1 ==
Section 1 text
== Section 2 ==
Section 2 text
=== Other Section ===
Section 3 text"""

    def test_get_section_info_from_page_first(self):
        section_id, section = mr.get_section_info_from_page(self.page_text, "Section 1")
        self.assertEqual(section_id, 1)
        self.assertEqual(section.title.strip(), "Section 1")
        self.assertEqual(section.plain_text().strip(), "== Section 1 ==\nSection 1 text")

    def test_get_section_info_from_page_middle(self):
        section_id, section = mr.get_section_info_from_page(self.page_text, "Section 2")
        self.assertEqual(section_id, 2)
        self.assertEqual(section.title.strip(), "Section 2")
        expected_text = "== Section 2 ==\nSection 2 text\n=== Other Section ===\nSection 3 text"
        self.assertEqual(section.plain_text().strip(), expected_text)

    def test_get_section_info_from_page_last(self):
        section_id, section = mr.get_section_info_from_page(self.page_text, "Other Section")
        self.assertEqual(section_id, 3)
        self.assertEqual(section.title.strip(), "Other Section")
        self.assertEqual(section.plain_text().strip(), "=== Other Section ===\nSection 3 text")

    def test_get_section_info_from_page_none(self):
        self.assertRaises(RuntimeError, mr.get_section_info_from_page, self.page_text, "Wrong Section")

    def test_get_section_info_from_page_loose(self):
        section_id, section = mr.get_section_info_from_page(self.page_text, "section 1", True)
        self.assertEqual(section_id, 1)
        self.assertEqual(section.title.strip(), "Section 1")
        self.assertEqual(section.plain_text().strip(), "== Section 1 ==\nSection 1 text")

        self.assertRaises(RuntimeError, mr.get_section_info_from_page, self.page_text, "section", True)

        section_id, section = mr.get_section_info_from_page(self.page_text, "other", True)
        self.assertEqual(section_id, 3)
        self.assertEqual(section.title.strip(), "Other Section")
        self.assertEqual(section.plain_text().strip(), "=== Other Section ===\nSection 3 text")

        section_id, section = mr.get_section_info_from_page(self.page_text, "Other Section", True)
        self.assertEqual(section_id, 3)
        self.assertEqual(section.title.strip(), "Other Section")
        self.assertEqual(section.plain_text().strip(), "=== Other Section ===\nSection 3 text")

if __name__ == '__main__':
    unittest.main()

import unittest

import commands.distroinfo.utils.distro_page_distroinfo as dpd

class TestDistroPageDistroInfo(unittest.TestCase):
    def test_remove_ctp_from_type(self):
        new_type = dpd.remove_ctgp_from_type("[[Riivolution]]")
        self.assertEqual(new_type, "[[Riivolution]]")

        new_type = dpd.remove_ctgp_from_type("[[Riivolution]], [[CTGP Revolution]]")
        self.assertEqual(new_type, "[[Riivolution]], [[My Stuff]]")

        new_type = dpd.remove_ctgp_from_type("[[My Stuff]], [[CTGP Revolution]]")
        self.assertEqual(new_type, "[[My Stuff]]")

        new_type = dpd.remove_ctgp_from_type("[[CTGP Revolution]], [[My Stuff]]")
        self.assertEqual(new_type, "[[My Stuff]]")

        new_type = dpd.remove_ctgp_from_type("[[CTGP Revolution]], [[My Stuff]], [[Riivolution]]")
        self.assertEqual(new_type, "[[My Stuff]], [[Riivolution]]")

        new_type = dpd.remove_ctgp_from_type("[[Riivolution]], [[CTGP Revolution]], [[My Stuff]]")
        self.assertEqual(new_type, "[[Riivolution]], [[My Stuff]]")

if __name__ == '__main__':
    unittest.main()

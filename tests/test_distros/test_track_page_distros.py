import unittest
import warnings

import commands.distros.track_page_distros as tpd

class TestTrackPageHandler(unittest.TestCase):
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
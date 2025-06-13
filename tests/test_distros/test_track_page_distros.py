import unittest
import warnings

import commands.distros.track_page_distros as tpd

class TestTrackPageHandler(unittest.TestCase):
    def test_read_distro_name_wiikilink(self):
        distro_text = "[[Distro Name]]"
        distro_name = tpd.read_distro_name(distro_text)
        self.assertEqual(distro_name, "Distro Name")

    def test_read_distro_name_wiikilink_plus(self):
        distro_text = "[[Distro Name]] (v2.0)"
        distro_name = tpd.read_distro_name(distro_text)
        self.assertEqual(distro_name, "Distro Name")
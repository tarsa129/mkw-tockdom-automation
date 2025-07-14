import unittest

import commands.slotinfo.utils.reason_text_parse as rtp

class TestReasonTextParse(unittest.TestCase):
    def test_find_audience_sfx(self):
        self.assertTrue(rtp.find_audience_sfx("the audience SFX"))
        self.assertTrue(rtp.find_audience_sfx("the {{obj-ref|0xd|audience}}"))
        self.assertFalse(rtp.find_audience_sfx("commerce"))

    def test_find_cow_and_bell(self):
        self.assertTrue(rtp.find_cow_and_bell("the cow and bell sounds during the intro cameras"))
        self.assertFalse(rtp.find_cow_and_bell("commerce"))

    def test_find_snow_effect(self):
        self.assertTrue(rtp.find_snow_effect("the snow effect"))
        self.assertTrue(rtp.find_snow_effect("the {{obj-ref|0x2ef|snow effect}}"))
        self.assertFalse(rtp.find_snow_effect("thesnoweffect"))
        self.assertFalse(rtp.find_snow_effect("commerce"))

    def test_find_fog(self):
        self.assertTrue(rtp.find_fog("the fog effect"))
        self.assertFalse(rtp.find_fog("thefogeffect"))
        self.assertFalse(rtp.find_fog("commerce"))

    def test_find_pylon01(self):
        self.assertTrue(rtp.find_pylon01("the {{obj-ref|0x144|pylons}}"))
        self.assertTrue(rtp.find_pylon01("the object {{obj-ref|0x144|pylon01}}"))
        self.assertFalse(rtp.find_pylon01("commerce"))

    def test_find_sun_ds(self):
        self.assertTrue(rtp.find_sun_ds("the object {{obj-ref|0x72|sunds}}"))
        self.assertTrue(rtp.find_sun_ds("the {{obj-ref|0x72|angry sun}}"))
        self.assertFalse(rtp.find_sun_ds("commerce"))

    def test_find_rr_sticky_read_sfx(self):
        self.assertTrue(rtp.find_rr_sticky_read_sfx("[[kcl flag#sticky road (0x16) %5battach%5d|road sfx]]"))
        self.assertTrue(rtp.find_rr_sticky_read_sfx("the [[kcl flag#16|road sfx]]"))
        self.assertFalse(rtp.find_rr_sticky_read_sfx("commerce"))

    def test_find_rr_road_2_sfx(self):
        self.assertTrue(rtp.find_rr_road_2_sfx("the [[kcl flag#17|road sfx]]"))
        self.assertTrue(rtp.find_rr_road_2_sfx("[[kcl flag#Road 2 (0x17)|road]]"))
        self.assertFalse(rtp.find_rr_road_2_sfx("[[kcl flag#sticky road (0x16) %5battach%5d|road sfx]]"))
        self.assertFalse(rtp.find_rr_road_2_sfx("commerce"))

    def test_find_rr_special_wall_sfx(self):
        self.assertTrue(rtp.find_rr_special_wall_sfx("[[kcl flag#1e|wall SFX]]"))
        self.assertTrue(rtp.find_rr_special_wall_sfx("[[kcl flag#1e|special wall kcl flag]]"))
        self.assertTrue(rtp.find_rr_special_wall_sfx("[[kcl flag#special Wall (0x1e)|wall sfx]]"))
        self.assertFalse(rtp.find_rr_special_wall_sfx("commerce"))

    def test_find_reason_in_clause(self):
        clause_text = "the use of Cataquacks without [[Psea]]"
        self.assertEqual(rtp.find_reason_in_clause(clause_text), "cataquacks-no-psea")

    def test_reason_text_parse(self):
        reason_text = "commerce "
        actual_reasons = rtp.parse_reasons(reason_text)
        expected_reasons = {"reason": "the commerce"}
        self.assertDictEqual(actual_reasons, expected_reasons)

    def test_reason_text_cow_bell(self):
        reason_text = "cow and bell sounds and commerce"
        actual_reasons = rtp.parse_reasons(reason_text)
        expected_reasons = {"reason":"cow-bells", "reason2": "the commerce"}
        self.assertDictEqual(actual_reasons, expected_reasons)

    def test_reason_text_parse_list(self):
        reason_text = "the [[KCL flag#17|road SFX]], [[KCL flag#1E|wall SFX]] and [[KCL flag#18|sound triggers]]"
        actual_reasons = rtp.parse_reasons(reason_text)
        expected_reasons = {"reason": "rr-road-2-sfx", "reason2": "rr-special-wall-sfx", "reason3": "sound-triggers"}
        self.assertDictEqual(actual_reasons, expected_reasons)

    def test_reason_text_parse_already_parsed(self):
        reason_text = "sound-triggers"
        actual_reasons = rtp.parse_reasons(reason_text)
        self.assertIsNone(actual_reasons)

    def test_reason_text_parse_unique_the(self):
        reason_text = "the commerce"
        actual_reasons = rtp.parse_reasons(reason_text)
        expected_reasons = {"reason": "the commerce"}
        self.assertDictEqual(actual_reasons, expected_reasons)

if __name__ == '__main__':
    unittest.main()

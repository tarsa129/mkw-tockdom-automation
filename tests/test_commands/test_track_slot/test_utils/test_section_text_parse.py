import unittest

import commands.slotinfo.utils.section_text_parse as stp

class TestSlotTrackPageRead(unittest.TestCase):
    def test_read_slot_text_basic(self):
        section_text = "It is recommended to put this track on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]]."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot": "5.2"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_arena(self):
        section_text = "It is recommended to put this arena on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]]."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"type":"arena", "slot": "5.2"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_mandatory(self):
        section_text = "It is mandatory to put this track on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]]."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"advice":"mandatory", "slot": "5.2"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_notrecommended(self):
        section_text = "It is not recommended to put this track on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]]."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"advice":"not-recommended", "slot": "5.2"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_willwork(self):
        section_text = "This track will work on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]]."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"advice":"will-work", "slot": "5.2"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_willnotwork(self):
        section_text = "This track will not work on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]]."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"advice":"not-work", "slot": "5.2"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_willonlywork(self):
        section_text = "This track will only work on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]]."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"advice":"only-work", "slot": "5.2"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_slot_text(self):
        section_text = "It is recommended to put this track on the [[Slot#7.3|<small>N64</small> DK's Jungle Parkway slot]] or the [[Slot#8.3|<small>GCN</small> DK Mountain slot]] because of the dirt GFX."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot": "7.3", "slot2": "8.3", "reason":"the dirt GFX"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_slot_basic(self):
        section_text = "It is recommended to put this track on [[slot]] [[slot#6.4|6.4]]."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot": "6.4"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_versions_four(self):
        section_text = 'It is recommended to put this track on the [[Slot#battle1.1|Grumble Volcano slot]], [[Slot#2.2|Grumble Volcano slot]], [[Slot#3.3|Grumble Volcano slot]], or [[Slot#4.4|<small>ds</small>Grumble Volcano slot]].'
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot":"battle1.1", "slot2":"2.2", "slot3":"3.3", "slot4":"4.4"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_reason(self):
        section_text = "It is recommended to put this track on the [[Slot#1.2|Moo Moo Meadows slot]] because of the cow and bell sounds during the intro cameras."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot":"1.2", "reason":"the cow and bell sounds during the intro cameras"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_version_single(self):
        section_text = "It is recommended to put this track on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]] in v1.1."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot": "5.2", "version-subset":"single", "version":"v1.1"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_version_range(self):
        section_text = "It is recommended to put this track on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]] in Beta 1 to Beta End."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot": "5.2", "version-subset":"range", "version":"Beta 1", "version2":"Beta End"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_version_arbitrary(self):
        section_text = "It is recommended to put this track on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]] in Beta 1 and Beta 2."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot": "5.2", "version-subset":"arbitrary", "version":"Beta 1", "version2":"Beta 2"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_version_arbitrary_three(self):
        section_text = "It is recommended to put this track on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]] in Beta 1, Beta 2 and Beta 3."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot": "5.2", "version-subset":"arbitrary",
                         "version":"Beta 1", "version2":"Beta 2", "version3":"Beta 3"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_version_arbitrary_four(self):
        section_text = "It is recommended to put this track on the [[Slot#5.2|<small>DS</small> Yoshi Falls slot]] in Beta 1, Beta 2, Beta 3, and Beta 10."
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot": "5.2", "version-subset":"arbitrary",
                         "version":"Beta 1", "version2":"Beta 2", "version3":"Beta 3", "version4":"Beta 10"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_music(self):
        section_text = 'It is recommended to put this track on the [[Slot#6.4|<small>GCN</small> Waluigi Stadium slot]]. If used in a distribution that supports custom music slots, it is recommended to use the [[Slot#battle1.3|Funky Stadium music slot]].'
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"slot":"6.4", "music-slot":"battle1.3"}
        self.assertDictEqual(actual_info, expected_info)

    def test_read_slot_text_all(self):
        section_text = 'It is not recommended to put this arena on the [[Slot#3.4|Grumble Volcano slot]], [[Slot#1.1|Grumble Volcano slot]], [[Slot#4.4|Grumble Volcano slot]], or [[Slot#7.4|<small>ds</small>Grumble Volcano slot]] in v1.1, v1.2, v2.3, and v.5 for the sound triggers. If used in a distribution that supports custom music slots, it is recommended to use the [[Slot#battle1.4|Grumble Volcano slot]], [[Slot#battle2.1|Grumble Volcano slot]], [[Slot#3.4|Grumble Volcano slot]], or [[Slot#5.4|Grumble Volcano slot]].'
        actual_info = stp.read_slot_text(section_text)
        expected_info = {"advice":"not-recommended", "type":"arena",
                        "slot":"3.4", "slot2":"1.1", "slot3":"4.4", "slot4":"7.4",
                         "version-subset":"arbitrary", "version":"v1.1", "version2":"v1.2", "version3":"v2.3", "version4":"v.5",
                         "reason":"the sound triggers",
                         "music-slot":"battle1.4", "music-slot2":"battle2.1", "music-slot3":"3.4", "music-slot4":"5.4"}
        self.assertDictEqual(actual_info, expected_info)

if __name__ == '__main__':
    unittest.main()

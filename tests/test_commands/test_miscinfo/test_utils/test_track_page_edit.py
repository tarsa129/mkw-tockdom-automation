import unittest

import commands.miscinfo.utils.track_page_edit as tpe

class TestMiscInfoTrackPageEdit(unittest.TestCase):
    def test_patch_ids_to_miscinfo_template_new_track(self):
        arguments = {"wbz-id":"", "image-id": None}
        new_arguments = {"wbz-id":"123", "image-id": "123"}
        expected_args = {"wbz-id":"123", "image-id": None}
        tpe.patch_ids_to_miscinfo_template(arguments, new_arguments)
        self.assertDictEqual(expected_args, arguments)

    def test_patch_ids_to_miscinfo_template_new_update(self):
        arguments = {"wbz-id":"123", "image-id": None}
        new_arguments = {"wbz-id": "123", "image-id": "124"}
        expected_args = {"wbz-id": "123", "image-id": "124"}
        tpe.patch_ids_to_miscinfo_template(arguments, new_arguments)
        self.assertDictEqual(expected_args, arguments)

    def test_patch_ids_to_miscinfo_template_fake_update(self):
        arguments = {"wbz-id":"123", "image-id": None}
        new_arguments = {"wbz-id": "123", "image-id": "123"}
        expected_args = {"wbz-id": "123", "image-id": None}
        tpe.patch_ids_to_miscinfo_template(arguments, new_arguments)
        self.assertDictEqual(expected_args, arguments)

    def test_patch_ids_to_miscinfo_template_new_wbz(self):
        arguments = {"wbz-id":"122", "image-id": None}
        new_arguments = {"wbz-id": "123", "image-id": "123"}
        expected_args = {"wbz-id": "123", "image-id": None}
        tpe.patch_ids_to_miscinfo_template(arguments, new_arguments, True)
        self.assertDictEqual(expected_args, arguments)


if __name__ == '__main__':
    unittest.main()

import unittest
import warnings
from unittest import mock

from commands.miscinfo.action import edit_ids_on_page as eiop

class TestEditWbzIdsOnPage(unittest.TestCase):
    @mock.patch("commands.miscinfo.action.edit_ids_on_page.get_imagehash_by_id")
    def test_is_image_update(self, mock_get_imagehash_by_id):
        mock_get_imagehash_by_id.return_value = "hash2"
        arguments = {"wbz-id": 1, "image-id": None}
        new_image_hash = "hash1"

        is_image_update = eiop.is_image_update(arguments, new_image_hash)
        self.assertTrue(is_image_update)
        mock_get_imagehash_by_id.assert_called_once()

    @mock.patch("commands.miscinfo.action.edit_ids_on_page.get_imagehash_by_id")
    def test_is_image_same_hash(self, mock_get_imagehash_by_id):
        mock_get_imagehash_by_id.return_value = "hash1"
        arguments = {"wbz-id": 1, "image-id": 2}
        new_image_hash = "hash1"

        with warnings.catch_warnings(record=True) as w:
            is_image_update = eiop.is_image_update(arguments, new_image_hash)
        self.assertFalse(is_image_update)
        mock_get_imagehash_by_id.assert_called_once()

    @mock.patch("commands.miscinfo.action.edit_ids_on_page.get_imagehash_by_id")
    def test_is_image_update_new_track(self, mock_get_imagehash_by_id):
        mock_get_imagehash_by_id.return_value = "hash2"
        arguments = {"wbz-id": None, "image-id": None}
        new_image_hash = "hash1"

        is_image_update = eiop.is_image_update(arguments, new_image_hash)
        self.assertTrue(is_image_update)
        mock_get_imagehash_by_id.assert_not_called()


if __name__ == '__main__':
    unittest.main()

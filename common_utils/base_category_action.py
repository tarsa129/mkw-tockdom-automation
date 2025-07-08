from common_utils.file_writer import write_csv_file
from tockdomio import tockdomread, tockdomread_category
from constants import UPDATE_COUNT

class BaseCategoryAction:
    def __init__(self, action_function):
        self.action = action_function

    def action_from_entry(self, page_entry, **kwargs):
        page_id = page_entry["pageid"]
        page_name = page_entry["title"]
        page_text: str = page_entry["revisions"][0]["slots"]["main"]["content"]
        return self.action(page_id, page_name, page_text, **kwargs)

    def action_from_pagename(self, page_name, **kwargs):
        tockdom_response = tockdomread.get_page_text_by_name(page_name)
        self.action_from_entry(tockdom_response, **kwargs)

    def action_from_category_single(self, page_entry, **kwargs):
        try:
            return self.action_from_entry(page_entry, **kwargs)
        except Exception as e:
            return None

    def action_from_category(self, category_name, bulk_count=UPDATE_COUNT, skip_until=None, **kwargs):
        success_count = 0
        for page_entry in tockdomread_category.get_page_entries_of_category(category_name, skip_until):
            was_successful = self.action_from_category_single(page_entry, **kwargs)
            if was_successful:
                success_count += 1
            if success_count >= bulk_count:
                break

    def action_from_category_dump(self, category_name, bulk_count=UPDATE_COUNT, skip_until=None, dump_file_path=None, **kwargs):
        entries_to_write = []

        for page_entry in tockdomread_category.get_page_entries_of_category(category_name, skip_until):
            entry_to_write = self.action_from_category_single(page_entry, **kwargs)
            if entry_to_write:
                entries_to_write.extend(entry_to_write)
            if len(entries_to_write) >= bulk_count:
                break

        if entries_to_write:
            write_csv_file(dump_file_path, entries_to_write)

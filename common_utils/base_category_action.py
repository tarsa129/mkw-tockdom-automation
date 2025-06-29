from tockdomio import tockdomread, tockdomread_category
from constants import UPDATE_COUNT

class BaseCategoryAction:
    def __init__(self, action_function):
        self.action = action_function

    def action_from_entry(self, page_entry):
        page_id = page_entry["pageid"]
        page_name = page_entry["title"]
        page_text: str = page_entry["revisions"][0]["slots"]["main"]["content"]
        return self.action(page_id, page_name, page_text)

    def action_from_pagename(self, page_name):
        tockdom_response = tockdomread.get_page_text_by_name(page_name)
        self.action_from_entry(tockdom_response)

    def action_from_category_single(self, page_entry):
        try:
            return self.action_from_entry(page_entry)
        except Exception as e:
            return False

    def action_from_category(self, category_name, bulk_count=UPDATE_COUNT, skip_until=None):
        success_count = 0
        for page_entry in tockdomread_category.get_page_entries_of_category(category_name, skip_until):
            was_successful = self.action_from_category_single(page_entry)
            if was_successful:
                success_count += 1
            if success_count >= bulk_count - 1:
                break
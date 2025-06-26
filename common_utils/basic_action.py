from tockdomio import tockdomread, tockdomread_category
from constants import UPDATE_COUNT

class BasicAction:
    def __init__(self, action_function):
        self.action = action_function

    def action_from_entry(self, page_entry):
        page_id = page_entry["pageid"]
        page_name = page_entry["title"]
        page_text: str = page_entry["revisions"][0]["slots"]["main"]["content"]
        self.action(page_id, page_name, page_text)

    def action_from_pagename(self, page_name):
        tockdom_response = tockdomread.get_page_text_by_name(page_name)
        self.action_from_entry(tockdom_response)

    def action_from_category(self, category_name, bulk_count=UPDATE_COUNT):
        success_count = 0
        for page_entry in tockdomread_category.get_page_entries_of_category(category_name):
            try:
                self.action_from_entry(page_entry)
                success_count += 1
            except Exception as e:
                continue
            if success_count >= bulk_count - 1:
                break
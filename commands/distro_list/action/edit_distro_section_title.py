from common_utils.base_category_action import BaseCategoryAction

def edit_section_title(page_id, page_name, page_text, **kwargs):
    print(page_id, page_name, page_text, kwargs)
    return True

def edit_section_title_by_category(category, skip_until, old_section_title, new_section_title):
    action = BaseCategoryAction(edit_section_title)
    kwargs = {"old_section_title": old_section_title, "new_section_title": new_section_title}
    return action.action_from_category(category_name=category, skip_until=skip_until, **kwargs)
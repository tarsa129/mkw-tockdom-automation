from commands.distro_list.utils.distro_section_contents import edit_initial_line
from commands.distro_list.utils.distro_section_meta import get_distrosectioninfo_from_page
from common_utils.base_category_action import BaseCategoryAction
from constants import DISTRIBUTION_SECTION_TITLE
from tockdomio import tockdomwrite


def edit_section_title(page_id, page_name, page_text, **kwargs):
    section_id, distro_section = get_distrosectioninfo_from_page(page_text)

    new_contents = distro_section.contents
    update_first_line = "update_first_line" in kwargs and kwargs["update_first_line"]
    if update_first_line:
        track_type = kwargs["track_type"]
        new_contents = edit_initial_line(distro_section.contents, track_type)

    title_converted = distro_section.title.strip() == DISTRIBUTION_SECTION_TITLE.strip()
    if title_converted and new_contents == distro_section.contents:
        return False

    distro_section.title = DISTRIBUTION_SECTION_TITLE
    distro_section.contents = new_contents

    section_text = str(distro_section)
    print(section_text)

    response = tockdomwrite.edit_section(page_id, section_id, section_text, "Make Distro section generic (via API)")
    print(response.json())
    was_successful = response.json()["edit"]["result"] == "Success"
    return was_successful

def edit_section_title_by_category(category, skip_until):
    action = BaseCategoryAction(edit_section_title)
    kwargs = {"track_type": category.split("/")[0], "update_first_line": False}
    return action.action_from_category(category_name=category, skip_until=skip_until, **kwargs)
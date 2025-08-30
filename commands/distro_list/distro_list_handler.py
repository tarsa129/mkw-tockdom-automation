from common_utils.base_handler import BaseHandler
from .action.create_distros_file import create_trackdistro_file
from .action.edit_distros_list import edit_distros_from_file
from .action.edit_distros_file import edit_distros_list
from .action.edit_distro_section_title import edit_section_title_by_category

from .utils.distro_list_enums import Action


handler = BaseHandler()
handler.add_action("add", action_function = edit_distros_from_file,
                   args=({"name": "distro_file", "description": "The file that defines which pages should be updated with which distros."},
                       Action.ADD))
handler.add_action("update", action_function = edit_distros_from_file,
                   args=({"name": "distro_file", "description": "The file that defines which pages should be updated with which distros."},
                       Action.UPDATE))
handler.add_action("delete", action_function = edit_distros_from_file,
                   args=({"name": "distro_file", "description": "The file that defines which pages should be updated with which distros."},
                       Action.DELETE))
handler.add_action("create_file", action_function = create_trackdistro_file,
                   args=({"name": "distro_file", "description": "The file that defines which file to write the wiiki pages / distros to."},
                         {"name": "wiikipage", "description": "The wiikipage of the distribution."}))
handler.add_action("fix_file", action_function = edit_distros_list,
                   args=({"name": "distro_file", "description": "The file that defines which file with wiiki pages / distros that should be fixed."},
                         {"name": "distro_text", "description": "The text for the distribution that should be added to the file / each page."},
                         {"name": "fix_flags", "description": "Which edits to make on the file."}))
handler.add_action("convert_track_list", action_function = edit_section_title_by_category,
                   args=({"name": "category_name", "description": "Category name to edit pages."},
                         {"name": "skip_until", "description": "Page name to skip until"}
                         ))
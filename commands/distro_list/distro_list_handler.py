from .action.create_distros_file import create_trackdistro_file
from .action.edit_distros_list import edit_distros_to_pagenames
from .action.edit_distros_file import edit_distros_list
from .utils import distro_file_reader as distro_file

from .utils.distro_list_enums import Action

def handle_command(args):
    action = args["action"]
    file = args["distro-file"]

    if action == "add":
        pagename_to_distros = distro_file.read_distro_file(file)
        edit_distros_to_pagenames(pagename_to_distros, action = Action.ADD)
    elif action == "update":
        pagename_to_distros = distro_file.read_distro_file(file)
        edit_distros_to_pagenames(pagename_to_distros, action = Action.UPDATE)
    elif action == "delete":
        pagename_to_distros = distro_file.read_distro_file(file)
        edit_distros_to_pagenames(pagename_to_distros, action = Action.DELETE)
    elif action == "create_file":
        create_trackdistro_file(args["wiikipage"], file)
    elif action == "fix_file":
        distro_text = args["distro-text"]
        flags = args["fix-flags"]
        edit_distros_list(file, distro_text, flags)
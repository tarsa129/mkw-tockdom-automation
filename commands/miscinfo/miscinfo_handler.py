from commands.miscinfo.action.get_ids_from_szslibrary import get_wbz_ids


def handle_command(args):
    action = args["action"]
    if action == "get_ids":
        start_id = args["start_id"]
        end_id = args["end_id"]
        file_path = args["dump_file_path"]
        get_wbz_ids(start_id, end_id, file_path)

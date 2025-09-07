from common_utils.base_handler import BaseHandler
from commands.upload_files.action import upload_from_folder

handler = BaseHandler()
handler.add_action("folder", action_function = upload_from_folder.upload_files_from_folder,
                   args=("folder_name", ))
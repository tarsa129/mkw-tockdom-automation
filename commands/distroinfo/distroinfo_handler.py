from commands.distroinfo.action import convert_to_template as convert_to_template
from commands.distroinfo.action import fix_template
from common_utils.base_handler import BaseHandler

handler = BaseHandler()
handler.add_action("convert", action_function=convert_to_template.convert_by_category,
                   args=("category_name", "skip_until"))
handler.add_action("fix", action_function=fix_template.fix_by_category,
                   args=("category_name", "skip_until"))
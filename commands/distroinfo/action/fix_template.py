from common_utils.basic_action import BasicAction

def fix_template(page_id, page_name, page_text):
    print(page_id, page_name, page_text)

def get_action():
    return BasicAction(fix_template)
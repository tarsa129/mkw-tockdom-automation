from tockdomio import tockdomread

def add_distros(pageid, distros):
    page_text:str = tockdomread.get_page_text_by_id(pageid)


add_distros(1472, "")

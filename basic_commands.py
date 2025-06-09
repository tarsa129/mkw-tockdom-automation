from tockdomio import tockdomread
from trackpage import track_page

def add_distros(pageid, distros):
    page_text:str = tockdomread.get_page_text_by_id(pageid)["revisions"][0]["slots"]["main"]["content"]
    curr_distros = track_page.get_distros_from_page(page_text)
    print(curr_distros)

add_distros(1472, "")

from tockdomio import tockdomread
from trackpage import track_page

def add_distros(pageid, distros):
    page_text:str = tockdomread.get_page_text_by_id(pageid)["revisions"][0]["slots"]["main"]["content"]
    track_page.read_trackpage_from_text(page_text)

add_distros(1472, "")

from commands.distro_list.utils import distro_page_tracklist as distro_page
from tockdomio import tockdomread

def create_trackdistro_file(pagename, file):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)
    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    tracks = distro_page.get_tracklist_from_page(page_text)
    pass

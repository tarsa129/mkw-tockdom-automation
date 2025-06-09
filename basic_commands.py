from tockdomio import tockdomread
from trackpage import track_page
import warnings

def add_distros(pageid, new_distros: dict):
    page_text:str = tockdomread.get_page_text_by_id(pageid)["revisions"][0]["slots"]["main"]["content"]
    curr_distros = track_page.get_distros_from_page(page_text)

    invalid_new_distros = []
    for new_distro in new_distros:
        if new_distro in curr_distros:
            invalid_new_distros.append(new_distro)
            warnings.warn("{} already on the page!".format(new_distro))
    for invalid_distro in invalid_new_distros:
        new_distros.pop(invalid_distro)
    all_distros = curr_distros | new_distros
    all_distros = dict(sorted(all_distros.items(), key=lambda x: x[0].lower()))
    print(all_distros)

added_distros = {}
added_distros["tarsa's epic track page"] = "[[tarsa's epic track pack]] (v1.1)"
added_distros["CTGP"] = "{{Distrib-ref|Highlight Pack|11621|highlight-pack}}"
added_distros["OptPack"] = "{{Distrib-ref|Highlight Pack|11621|highlight-pack}}"
added_distros["Other Distro"] = "[[fun fun distro]]"
add_distros(1472, added_distros)

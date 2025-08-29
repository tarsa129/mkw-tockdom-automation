from commands.distro_list.utils.distribution_type import DistributionType
from mediawiki.mediawiki_read import get_section_info_from_page


def get_distrosectioninfo_from_page(page_text,
                                    distribution_type: DistributionType = None):
    if distribution_type is not None:
        return get_section_info_from_page(page_text, distribution_type.get_section_title())

    all_section_titles = DistributionType.get_all_section_titles()
    for section_title in all_section_titles:
        try:
            return get_section_info_from_page(page_text, section_title)
        except RuntimeError:
            continue
    raise RuntimeError("Track page has no valid distribution section!")

def get_distrosection_from_page(page_text,
                                distribution_type: DistributionType = DistributionType.CUSTOM_TRACK):
    _, section_text = get_distrosectioninfo_from_page(page_text, distribution_type)
    return section_text


def get_distros_sectionid(page_text, distribution_type = None):
    section_id, _ = get_distrosectioninfo_from_page(page_text, distribution_type)
    return section_id

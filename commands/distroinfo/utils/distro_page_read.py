from trackpage.wiiki_page_parse import get_first_section_from_page, read_table_sidecaption

def get_distroinfo_table(page_text):
    first_section = get_first_section_from_page(page_text)
    return read_table_sidecaption(first_section)

def get_distroinfo_template(page_text):
    first_section = get_first_section_from_page(page_text)
    return get_template_with_name(first_section, "Distribution-Info")
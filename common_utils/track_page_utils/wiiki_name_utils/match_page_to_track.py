import re
import warnings


class TrackPageName:
    def __init__(self, full_name, base_name, mod_type=None, authors=None):
        self.full_name = full_name
        self.base_name = base_name
        self.mod_type = mod_type
        self.authors = authors

    def check_modtype_authors(self, mod_type, authors):
        authors_converted = set([author.replace("_", " ") for author in authors])
        author_check = self.authors == authors_converted
        mod_type_check = mod_type == self.mod_type

        strict_check = author_check and mod_type_check
        #Authors are not always communicated in a page name, but mod type always is.
        loose_check = (self.authors is None or author_check) and (mod_type is None or mod_type_check)
        return loose_check, strict_check

    def check_authors(self, authors):
        return self.authors == authors

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.full_name == other.full_name and self.base_name == other.base_name \
                    and self.mod_type == other.mod_type and self.authors == other.authors
        else:
            return NotImplemented

    def __repr__(self):
        return f"{self.full_name}, {self.base_name}, {self.mod_type}, {self.authors}"

def get_parenthesis_groups(page_text):
    groups = []
    curr_group = ""
    page_text = page_text.strip()
    if not page_text.endswith(")"):
        return groups

    for s in page_text:
        if len(curr_group) == 0 and s == " ":
            continue

        curr_group += s
        if curr_group.count("(") == curr_group.count(")"):
            groups.append(curr_group)
            curr_group = ""

    return groups

def read_modification_type(paren_text):
    if paren_text.endswith(" Edit)"):
        return "Edit"
    elif paren_text.endswith(" Texture)"):
        return "Texture"
    return None

def read_authors(paren_text):
    return set(re.split(', | & ', paren_text[1:-1]))

# This will fail in the case that there is an author whose name edits with " Edit or " Texture".
# And this user creates a track that is NOT an edit or texture of something.
# Even if we did also check for the author names, it is possible for an author named "SNES Ghost Valley 2 Texture" to mess it up.
# This should be a rare occurrence that can be handled manually.
def read_parenthetical_groups(disambig_text):
    paren_groups = get_parenthesis_groups(disambig_text)

    mod_type = None
    authors = None

    if len(paren_groups) == 0:
        pass
    elif len(paren_groups) == 1:
        mod_type = read_modification_type(paren_groups[0])
        if not mod_type:
            authors = read_authors(paren_groups[0])
    elif len(paren_groups) == 2:
        mod_type = read_modification_type(paren_groups[0])
        authors = read_authors(paren_groups[1])
    elif len(paren_groups) > 2:
        warnings.warn(f"{disambig_text} has more than two () groups, which is invalid!")

    return mod_type, authors

def parse_page_name(page_name_text, base_name):
    if not page_name_text.startswith(base_name):
        return None
    track_page_name = TrackPageName(page_name_text, base_name)
    if page_name_text == base_name:
        return track_page_name
    parenthesis_groups = page_name_text[len(base_name):]
    track_page_name.mod_type, track_page_name.authors = read_parenthetical_groups(parenthesis_groups)

    return track_page_name
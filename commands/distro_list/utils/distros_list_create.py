import warnings
from collections import Counter

from commands.distro_list.utils.distro_list_enums import Action

# While duplicate distribution names are technically allowed, we still assume that all names are unique.
# At time of writing, only 4 such distributions exist, and only 1 is actually for tracks
# This one distribution does not have any overlapping tracks.
# Thus, is it more likely that duplicate distro names are a result of human error.
# In the future, if needed, we can revisit this by implementing this all as a dict of lists.
def validate_distros(distros: dict):
    distroname_counter = Counter(map(str.lower, distros.keys()))

    is_valid = True

    for distroname, distrocount in distroname_counter.most_common(len(distroname_counter)):
        if distrocount == 1:
            break
        is_valid = False
        warnings.warn("Distro with lowercase name {} appears more than once.".format(distroname))

    return is_valid


def combine_distros(curr_distros: dict, new_distros: dict, action):
    for new_distro, new_distro_text in new_distros.items():
        if new_distro in curr_distros:
            if action == Action.DELETE:
                curr_distros.pop(new_distro)
            elif action == Action.UPDATE:
                curr_distros[new_distro] = new_distro_text
            else:
                warnings.warn("{} already on the page!".format(new_distro))
        else:
            if action == Action.DELETE:
                warnings.warn("{} not on the page!".format(new_distro))
            else:
                curr_distros[new_distro] = new_distro_text
    return dict(sorted(curr_distros.items(), key=lambda x: x[0].lower()))

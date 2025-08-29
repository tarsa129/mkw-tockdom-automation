from enum import Enum

from constants import CUSTOM_TRACK_DISTRIBUTION, TRACK_EDIT_DISTRIBUTION, DISTRIBUTION_TITLE_BASE

class DistributionType(Enum):
    CUSTOM_TRACK = CUSTOM_TRACK_DISTRIBUTION
    TRACK_EDIT = TRACK_EDIT_DISTRIBUTION

    def get_section_title(self):
        return DISTRIBUTION_TITLE_BASE.format(self.value)

    @classmethod
    def get_all_section_titles(cls):
        return (
            cls.CUSTOM_TRACK.get_section_title(),
            cls.TRACK_EDIT.get_section_title()
        )
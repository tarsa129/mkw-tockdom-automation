from common_utils.track_page_utils.template_utils.template_utils import TockdomTemplate


class SlotInfoTemplate(TockdomTemplate):
    template_name = "Slot-Info"
    required_params = ["slot"]

    def __init__(self):
        super().__init__()
        self.advice = None
        self.type = None
        self.slot = ""
        self.slot2 = None
        self.slot3 = None
        self.slot4 = None
        self.version_subset = None
        self.version = None
        self.version2 = None
        self.version3 = None
        self.version4 = None
        self.reason = None
        self.reason2 = None
        self.reason3 = None
        self.reason4 = None
        self.reason5 = None
        self.reason6 = None
        self.reason7 = None
        self.reason8 = None
        self.reason9 = None
        self.reason10 = None
        self.music_slot = None
        self.music_slot2 = None
        self.music_slot3 = None
        self.music_slot4 = None

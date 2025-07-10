import re

IT_IS_ADVICE_GROUP = 2
IT_IS_TYPE_GROUP = 3
THIS_WILL_TYPE_GROUP = 4
THIS_WILL_ADVICE_GROUP = 5
SLOT_GROUP = 6
SLOT2_GROUP = 9
SLOT3_GROUP = 12
SLOT4_GROUP = 15
VERSION_GROUP = 18
VERSION_END_GROUP = 21
VERSION2_GROUP = 24
VERSION3_GROUP = 26
VERSION4_GROUP = 28
REASON_GROUP = 31
MUSIC_SLOT_GROUP = 33
MUSIC_SLOT2_GROUP = 36
MUSIC_SLOT3_GROUP = 39
MUSIC_SLOT4_GROUP = 42


def get_advice_type(slot_info_match) -> dict:
    template_info = {}
    if slot_info_match.group(IT_IS_TYPE_GROUP) and slot_info_match.group(IT_IS_TYPE_GROUP) == "arena":
        template_info["type"] = "arena"
    elif slot_info_match.group(THIS_WILL_ADVICE_GROUP) and slot_info_match.group(THIS_WILL_ADVICE_GROUP) == "arena":
        template_info["type"] = "arena"

    if slot_info_match.group(IT_IS_ADVICE_GROUP):
        advice_text = slot_info_match.group(IT_IS_ADVICE_GROUP)
        if advice_text == "mandatory":
            template_info["advice"] = "mandatory"
        elif advice_text == "not recommended":
            template_info["advice"] = "not-recommended"
    elif slot_info_match.group(THIS_WILL_ADVICE_GROUP):
        advice_text = slot_info_match.group(THIS_WILL_ADVICE_GROUP)
        if advice_text == "will work":
            template_info["advice"] = "will-work"
        elif advice_text == "will not work":
            template_info["advice"] = "not-work"
        elif advice_text == "will only work":
            template_info["advice"] = "only-work"

    return template_info

def validate_slot(slot_text):
    slot_re = "(battle)?([1-8])\.([1-5])"
    slot_match = re.search(slot_re, slot_text)
    if not slot_match:
        return False

    first_number = int(slot_match.group(2))
    second_number = int(slot_match.group(3))
    if slot_match.group(1) and slot_match.group(1) == "battle" and first_number > 2:
        return False
    elif not slot_match.group(1) and second_number > 4:
        return False
    return True

def get_slots(slot_info_match, group_ids, arg_names):
    template_info = {}
    def get_slot_value(slot_group):
        slot_text = slot_info_match.group(slot_group)
        if slot_text and not validate_slot(slot_text):
            raise RuntimeError(f"Slot with group {slot_group} is not valid.")
        return slot_text

    if not slot_info_match.group(group_ids[0]):
        return template_info

    for i in range(len(group_ids)):
        if slot_info_match.group(group_ids[i]):
            template_info[arg_names[i]] = get_slot_value(group_ids[i])
    return template_info

def get_track_slots(slot_info_match) -> dict:
    return get_slots(slot_info_match, (SLOT_GROUP, SLOT2_GROUP, SLOT3_GROUP, SLOT4_GROUP),
                     ("slot", "slot2", "slot3", "slot4"))

def get_versions(slot_info_match) -> dict:
    template_info = {}

    version_text = slot_info_match.group(VERSION_GROUP)
    if not version_text:
        return template_info
    template_info["version-subset"] = "single"
    template_info["version"] = version_text

    version_end_text = slot_info_match.group(VERSION_END_GROUP)
    version2_text = slot_info_match.group(VERSION2_GROUP)
    version3_text = slot_info_match.group(VERSION3_GROUP)
    version4_text = slot_info_match.group(VERSION4_GROUP)

    if version_end_text:
        template_info["version-subset"] = "range"
        template_info["version2"] = version_end_text
    elif version2_text or version3_text or version4_text:
        template_info["version-subset"] = "arbitrary"
        if not version2_text:
            template_info["version2"] = version4_text
        elif not version3_text:
            template_info["version2"] = version2_text
            template_info["version3"] = version4_text
        else:
            template_info["version2"] = version2_text
            template_info["version3"] = version3_text
            template_info["version4"] = version4_text

    return template_info

def get_reason(slot_info_match):
    template_info = {}
    if slot_info_match.group(REASON_GROUP):
        template_info["reason"] = slot_info_match.group(REASON_GROUP)
    return template_info


def get_music_slots(slot_info_match):
    return get_slots(slot_info_match, (MUSIC_SLOT_GROUP, MUSIC_SLOT2_GROUP, MUSIC_SLOT3_GROUP, MUSIC_SLOT4_GROUP),
                     ("music-slot", "music-slot2", "music-slot3", "music-slot4"))

def read_slot_text(section_text):
    advice_type_regex = "^(It is (recommended|mandatory|not recommended) to put this (track|arena)|This (track|arena) (will work|will not work|will only work)) on the \[\[Slot#((battle)?[1-8]\.[1-4])\|[a-zA-Z<\/> 0-9']{0,40}slot]](, \[\[Slot#((battle)?[1-8]\.[1-4])\|[a-zA-Z<\/> 0-9']{0,40}slot]])?(, \[\[Slot#((battle)?[1-8]\.[1-4])\|[a-zA-Z<\/> 0-9']{0,40}slot]])?(,? or the \[\[Slot#((battle)?[1-8]\.[1-4])\|[a-zA-Z<\/> 0-9']{0,40}slot]])?( in ([^,]{0,10})(( to ([^,]{0,10}))|((, ([^,]{0,10}))?(, ([^,]{0,10}))?(,? and (.{0,10}))?)))?( (because of|for) (the .{0,120}))?\.( If used in a distribution that supports custom music slots, it is recommended to use the \[\[Slot#((battle)?[1-8]\.[1-4])\|[a-zA-Z<\/> 0-9']{0,40}slot]](, \[\[Slot#((battle)?[1-8]\.[1-4])\|[a-zA-Z<\/> 0-9']{0,40}slot]])?(, \[\[Slot#((battle)?[1-8]\.[1-4])\|[a-zA-Z<\/> 0-9']{0,40}slot]])?(,? or \[\[Slot#((battle)?[1-8]\.[1-4])\|[a-zA-Z<\/> 0-9']{0,40}slot]])?\.)?$"
    slot_info_match = re.search(advice_type_regex, section_text.strip())
    if not slot_info_match:
        raise RuntimeError("Page does not have a valid slot information text.")

    slot_template_info = {}
    slot_template_info |= get_advice_type(slot_info_match)
    slot_template_info |= get_track_slots(slot_info_match)
    slot_template_info |= get_versions(slot_info_match)
    slot_template_info |= get_reason(slot_info_match)
    slot_template_info |= get_music_slots(slot_info_match)
    return slot_template_info
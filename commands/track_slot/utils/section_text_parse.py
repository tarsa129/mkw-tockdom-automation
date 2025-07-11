import re

IT_IS_ADVICE_GROUP = 2
IT_IS_TYPE_GROUP = 3
THIS_WILL_TYPE_GROUP = 4
THIS_WILL_ADVICE_GROUP = 5

def get_advice_type(section_text) -> dict:
    advice_type_re = "^(It is (recommended|mandatory|not recommended) to put this (track|arena)|This (track|arena) (will work|will not work|will only work))"
    slot_info_match = re.search(advice_type_re, section_text)

    if not slot_info_match:
        raise RuntimeError("Not able to parse the advice and track type.")

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

def get_slots(section_text, arg_names):
    slot_full_re = "\[\[[sS]lot#((battle)?[1-8]\.[1-5])\|([a-zA-Z<\/> 0-9']{0,40}(slots?)?|((battle)?[1-8]\.[1-5]))?]]"
    slot_full_matches = re.findall(slot_full_re, section_text)
    if not slot_full_matches:
        raise RuntimeError(f"Text {section_text} does NOT match any known regexes.")

    matches = []

    for match in slot_full_matches:
        if validate_slot(match[0]):
            matches.append(match[0])
        elif validate_slot(match[4]):
            matches.append(match[4])
        else:
            raise RuntimeError(f"Text {match} does NOT match any known regexes.")


    match_dict = {}
    for i, match in enumerate(matches):
        match_dict[arg_names[i]] = match
    return match_dict


def get_track_slots(slot_info_match) -> dict:
    return get_slots(slot_info_match, ("slot", "slot2", "slot3", "slot4"))

def get_versions(section_text) -> dict:
    #this is the worst code i have ever written
    section_text = section_text[3:].strip(".")

    template_info = {}
    if " to " in section_text:
        version_split = section_text.split(" to ")
        template_info["version-subset"] = "range"
        template_info["version"] = version_split[0].strip()
        template_info["version2"] = version_split[1].strip()
        return template_info

    version_split = re.split(", and |, | and ", section_text)

    template_info["version-subset"] = "single" if len(version_split) == 1 else "arbitrary"
    template_info["version"] = version_split[0].strip()


    if len(version_split) > 1:
        template_info["version2"] = version_split[1].strip()
    if len(version_split) > 2:
        template_info["version3"] = version_split[2].strip()
    if len(version_split) > 3:
        template_info["version4"] = version_split[3].strip()

    return template_info

def get_reason(section_text):
    template_info = {"reason": section_text.strip(".")}
    return template_info


def get_music_slots(slot_info_match):
    return get_slots(slot_info_match,("music-slot", "music-slot2", "music-slot3", "music-slot4"))

def read_slot_text(section_text):
    slot_template_info = {}

    advice_type_split = re.split(" on the | on ", section_text)
    if len(advice_type_split) < 2:
        raise RuntimeError("Page does NOT have 'on the' or 'on' text, which is currently required for parsing.")
    advice_type_match = advice_type_split[0]
    slot_template_info |= get_advice_type(advice_type_match)
    remaining_text = advice_type_split[1].strip()

    sentence_split = re.split("\. ", remaining_text)
    if len(sentence_split) > 2:
        raise RuntimeError("Page has more than 3 sentences. This is not allowed.")

    first_sentence = sentence_split[0]

    slot_info_split = re.split(" in | because of | for | since | as | due to ", first_sentence)
    slot_template_info |= get_track_slots(slot_info_split[0])
    remaining_text = first_sentence[len(slot_info_split[0]):]

    if remaining_text:
        version_split = re.split(" because of | for | since | as | due to ", remaining_text)
        if version_split[0].strip().startswith("in "):
            slot_template_info |= get_versions(version_split[0].strip())

        if len(version_split) > 1 and version_split[1]:
            slot_template_info |= get_reason(version_split[1])

    if len(sentence_split) > 1:
        slot_template_info |= get_music_slots(sentence_split[1])
    return slot_template_info
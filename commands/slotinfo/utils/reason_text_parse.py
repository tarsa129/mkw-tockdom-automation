import re

#Only used to find common words that may be part of other words
def search_word_in_text(word, reason_text):
    return re.search("\\b" + word + "\\b", reason_text) is not None

def find_audience_sfx(reason_text):
    return"audience" in reason_text

def find_cow_and_bell(reason_text):
    return "cow and bell" in reason_text

def find_snow_effect(reason_text):
    return search_word_in_text("snow", reason_text)

def find_fog(reason_text):
    return search_word_in_text("fog", reason_text)

def find_pylon01(reason_text):
    return "pylon" in reason_text

def find_sun_ds(reason_text):
    return search_word_in_text("sun", reason_text) or "sunds" in reason_text

def find_fire_snake(reason_text):
    return "snake" in reason_text

def find_killer_rr_oob(reason_text):
    return "bullet bill" in reason_text

def find_ice(reason_text):
    return search_word_in_text("ice", reason_text)

def find_heyho_ship_gba(reason_text):
    return "heyhoshipgba" in reason_text or "shy guy ship" in reason_text

def find_heyho_ball_gba(reason_text):
    return "heyhoballgba" in reason_text or "cannonball" in reason_text

def find_music(reason_text):
    return "music" in reason_text

def find_sound_triggers(reason_text):
    return "sound trigger" in reason_text

def find_cannon_sfx(reason_text):
    return "cannon sfx" in reason_text

def find_waterfall_sfx(reason_text):
    return "waterfall sfx" in reason_text

def find_vehicle_invincibility(reason_text):
    return "invincibility" in reason_text

def find_rr_sticky_read_sfx(reason_text):
    return "%5battach%5d" in reason_text or "kcl flag#16" in reason_text

def find_rr_road_2_sfx(reason_text):
    if find_rr_sticky_read_sfx(reason_text):
        return False
    return "road sfx" in reason_text or ("road" in reason_text and "17" in reason_text)

def find_rr_special_wall_sfx(reason_text):
    return search_word_in_text("wall", reason_text) and "1e" in reason_text

def find_dirt_gfx(reason_text):
    return "dirt gfx" in reason_text

def find_launch_star_sfx(reason_text):
    return "launch_star" in reason_text or "starring" in reason_text

def find_cataquacks_no_psea(reason_text):
    return "cataquack" in reason_text and "psea" in reason_text


defined_reasons = {
    find_audience_sfx: "audience-sfx",
    find_cow_and_bell: "cow-bells",
    find_snow_effect: "snow",
    find_fog: "fog",
    find_pylon01: "pylon01",
    find_sun_ds: "sunDS",
    find_fire_snake: "fireSnake",
    find_killer_rr_oob: "rr-killer-oob",
    find_ice: "ice",
    find_heyho_ship_gba: "HeyhoShipGBA",
    find_heyho_ball_gba: "HeyhoBallGBA",
    find_music: "music",
    find_sound_triggers: "sound-triggers",
    find_cannon_sfx: "cannon-sfx",
    find_waterfall_sfx: "waterfall-sfx",
    find_vehicle_invincibility: "vehicle-invincibility",
    find_rr_sticky_read_sfx: "rr-sticky-road-sfx",
    find_rr_road_2_sfx: "rr-road-2-sfx",
    find_rr_special_wall_sfx: "rr-special-wall-sfx",
    find_dirt_gfx: "dirt-gfx",
    find_launch_star_sfx: "launch-star-sfx",
    find_cataquacks_no_psea: "cataquacks-no-psea"
}

def find_defined_reason(reason_text):
    reason_search = reason_text.lower()
    for defined_reason, defined_value in defined_reasons.items():
        if defined_reason(reason_search):
            return defined_value
    return None

def find_reason_in_clause(reason_text, edit_custom=True):
    defined_reason = find_defined_reason(reason_text)
    if defined_reason:
        return defined_reason
    if not edit_custom:
        return None
    if not reason_text.startswith("the "):
        return "the " + reason_text.strip()
    return reason_text.strip()

def parse_reasons(reason_text, edit_custom=True):
    if reason_text in defined_reasons.values():
        return None

    reason_clauses = re.split(", | and (?!bell)| or ", reason_text)
    reason_list = [find_reason_in_clause(reason_clause, edit_custom) for reason_clause in reason_clauses]
    if len(list(filter(lambda x: x is None, reason_list))) > 0:
        return None

    reason_args = {"reason": reason_list[0]}

    for i, reason in enumerate(reason_list[1:]):
        reason_args[f"reason{i+2}"] = reason

    return reason_args

def is_defined_reason(reason_text):
    return reason_text in defined_reasons.values()
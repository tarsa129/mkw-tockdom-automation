from common_utils.szslibrary_helpers import SZSLibraryTrackInfo, get_family_info


def get_wbz_id_from_miscinfo(family_id, misc_info_arguments):
    if str(family_id) != misc_info_arguments["wbz-id"]:
        return None

    track_infos: list[SZSLibraryTrackInfo] = get_family_info(family_id)
    #First, see which one matches the full version name
    for track_info in track_infos:
        if track_info.get_full_versionname() == misc_info_arguments["version"]:
            return track_info
        elif track_info.get_full_versionname() == misc_info_arguments["version"].replace(" ", ""):
            print(f"{family_id}:Matching with SZSLib version {track_info.get_full_versionname()} without spaces.")
            return track_info

    print(f"{family_id}: Could not find exact SZSLib match for {misc_info_arguments['version']}, searching for date {misc_info_arguments['date of release']} instead.")

    #If version names are unsynced (see TGAW), then we can go by the date
    matching_dates = list(filter(lambda x: x.track_created == misc_info_arguments["date of release"], track_infos))
    if not matching_dates:
        return None

    print(f"{family_id}: Found some match for {misc_info_arguments['date of release']}.")
    if len(matching_dates) == 1:
        return matching_dates[0]

    #if multiple track info entries match the date, take the latest official version.
    offcial_matching_dates = list(filter(lambda x: x.is_official_version(), matching_dates))
    if offcial_matching_dates:
        return offcial_matching_dates[-1]
    return matching_dates[-1]
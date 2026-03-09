import hashlib

from constants import SZSLIB_TRACK_AUTHOR, SZSLIB_TRACK_EDITOR
from tockdomio import szslibrary_read
from tockdomio.szslibrary_read import get_image_from_id

class SZSLibraryTrackInfo:
    id_first = 0
    track_wiki = 0
    prefix = ""
    trackname = ""
    track_version = ""
    track_version_extra = ""
    track_author = set()
    track_editor = set()
    track_family = 0
    track_clan = 0
    track_sha1 = ""
    track_created = ""
    track_wbz_size = 0
    track_warn = 0
    track_slot = ""
    track_prop = ""
    track_music = ""
    track_speed = 1
    track_laps = 3
    track_customtrack = 0
    track_customarena = 0
    track_texturehack = 0
    track_boost = 0
    track_competition = 0
    track_nintendo = 0
    track_change = 0

    @classmethod
    def from_szslibrary_response(cls, dict_response):
        track_info = cls()
        track_info.__dict__ = dict_response

        track_info.track_author = set(dict_response[SZSLIB_TRACK_AUTHOR].split(","))
        track_info.track_version_extra = track_info.track_version_extra or None

        track_editor_text = dict_response[SZSLIB_TRACK_EDITOR]
        if track_editor_text is None:
            track_info.track_updaters = set()
        else:
            track_info.track_updaters = set(track_editor_text.strip().split(","))

        track_info.track_customtrack = str(track_info.track_customtrack) == "1"
        track_info.track_customarena = str(track_info.track_customarena) == "1"
        track_info.track_texturehack = str(track_info.track_texturehack) == "1"
        track_info.track_competition = str(track_info.track_competition) == "1"
        track_info.track_nintendo = str(track_info.track_nintendo) == "1"
        track_info.track_change = str(track_info.track_change) == "1"

        return track_info

    def get_mod_type(self):
        if self.track_change:
            return "Edit"
        elif self.track_texturehack:
            return "Texture"
        return None

    def is_official_version(self):
        return self.track_version_extra is None

    def get_full_trackname(self):
        track_name = f"{self.trackname}".strip()
        prefix = self.prefix
        if prefix:
            track_name = f"{prefix} {track_name}"
        return track_name

    def get_full_versionname(self):
        version_name = f"{self.track_version}".strip()
        version_extra = self.track_version_extra
        if version_extra:
            version_name = f"{version_name}-{version_extra}"
        return version_name

    def get_full_trackname_version(self):
        track_name = self.get_full_trackname()
        version_name = self.get_full_versionname()
        return f"{track_name} {version_name}"

    def get_writeable_entry(self):
        return {"wbz_id": self.track_family, "image_id": self.id_first,
                "page_id": self.track_wiki, "track_name": self.get_full_trackname(), "track_version_extra": self.get_full_versionname(),
                "authors": self.track_author, "updaters": self.track_editor}

def validate_wbz_id(id_text):
    if not id_text.isnumeric():
        return False

    id_num = int(id_text)
    if id_num == 0:
        return False

    return True

def validate_start_end_wbz_ids(start_id, end_id):
    if not validate_wbz_id(start_id):
        raise RuntimeError(f"Start id {start_id} must be a positive integer")
    if not validate_wbz_id(end_id):
        raise RuntimeError(f"End id {end_id} must be a positive integer")

    start_id_num = int(start_id)
    end_id_num = int(end_id)

    if end_id_num < start_id_num:
        raise RuntimeError(f"Start id {start_id_num} cannot be greater than end id {end_id}")

    return True

def get_track_info(wbz_id):
    szslibrary_response = szslibrary_read.get_by_wbz_id(wbz_id)
    if not szslibrary_response or not szslibrary_response.get("track_info", None):
        return None

    return SZSLibraryTrackInfo.from_szslibrary_response(szslibrary_response["track_info"])

def get_imagehash_by_id(image_id):
    image_content = get_image_from_id(image_id)
    if image_content is None:
        return None

    return hashlib.sha256(str(image_content).encode()).hexdigest()
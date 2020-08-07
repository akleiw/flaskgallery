import unicodedata
from app import service, cache
from gphotospy.album import Album


def normalize_for_url(text: str):
    # spaces to underscores, remove parenthesis
    translation = str.maketrans(' ', '_', '()')
    text = unicodedata.normalize('NFD', text).encode(
        'ascii', 'ignore').decode('utf-8')
    text = text.translate(translation)
    return text

@cache.memoize()
def get_albums():
    album_manager = Album(service)
    return {normalize_for_url(a.get('title')): a for a in album_manager.list()}

import unicodedata
import string
from app import service, cache
from app import app
from gphotospy.album import Album
from gphotospy.media import Media, MediaItem


def normalize_for_url(text: str):
    # spaces and slashes to underscores, all other punctuation
    translation = str.maketrans(' /', '__', string.punctuation)
    text = unicodedata.normalize('NFD', text).encode(
        'ascii', 'ignore').decode('utf-8')  # replace special characters with their unicode counterparts
    text = text.translate(translation)
    return text


@cache.memoize()
def get_albums():
    app.logger.debug('gphotos.get_albums() executed')
    album_manager = Album(service)
    return {normalize_for_url(a.get('title')): a for a in album_manager.list()}


@cache.memoize()
def get_media(album_id):
    media_manager = Media(service)
    album_media_list = list(MediaItem(m)
                            for m in media_manager.search_album(album_id))
    return album_media_list

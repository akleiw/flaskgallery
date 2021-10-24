import unicodedata
import string
import urllib.request
import os
from sqlalchemy import delete
from flask_login import current_user
from app import service, cache
from app import app, db
from app.models import Album, Role
from gphotospy.album import Album as GPhotosAlbum
from gphotospy.media import Media, MediaItem


def normalize_for_url(text: str):
    # spaces and slashes to underscores, all other punctuation
    translation = str.maketrans(' /', '__', string.punctuation)
    text = unicodedata.normalize('NFD', text).encode(
        'ascii', 'ignore').decode('utf-8')  # replace special characters with their unicode counterparts
    text = text.translate(translation)
    return text



def get_albums():
    if current_user.is_anonymous:
        query = Role.get_public_role().albums
    else:
        query = current_user.albums()
    return {a.url_title: a for a in query}

def cache_albums(refresh_thumbnails=False):
    album_manager = GPhotosAlbum(service)
    current_ids = list()
    for a in album_manager.list():
        album = Album.query.filter_by(gphotos_id = a.get('id')).first()
        if not album:
            album = Album()
        album.gphotos_id = a.get('id')
        current_ids.append(a.get('id'))
        album.title = a.get('title')
        album.url_title = normalize_for_url(a.get('title'))
        album.items_count = a.get('mediaItemsCount')
        db.session.add(album)
        thumbnail = os.path.join(app.config['ALBUM_THUMB_PATH'], a.get('id') + '.jpg')
        if not os.path.exists(thumbnail) or refresh_thumbnails:
            urllib.request.urlretrieve(a.get('coverPhotoBaseUrl')+ "=w300-h200-c", os.path.join(app.config['ALBUM_THUMB_PATH'], a.get('id') + '.jpg'))

    # delete from db albums no longer in google photos
    stmt = delete(Album).where(Album.gphotos_id.notin_(current_ids)).execution_options(synchronize_session="fetch")
    db.session.execute(stmt)
    db.session.commit()

@cache.memoize()
def get_media(album_id):
    media_manager = Media(service)
    album_media_list = list(MediaItem(m)
                            for m in media_manager.search_album(album_id))
    return album_media_list

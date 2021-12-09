# pylint: disable=no-member
import os
import string
import unicodedata
import urllib.request
from datetime import datetime
from typing import Tuple

from flask_login import current_user
from gphotospy.album import Album as GPhotosAlbum
from gphotospy.media import Media, MediaItem, date
from sqlalchemy import delete

from app import app, cache, db, service
from app.models import Album, Role


def normalize_for_url(text: str):
    # spaces and slashes to underscores, all other punctuation
    translation = str.maketrans(" /", "__", string.punctuation)
    text = (
        unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
    )  # replace special characters with their unicode counterparts
    text = text.translate(translation)
    return text


def get_albums():
    if current_user.is_anonymous:
        query = Role.get_public_role().albums
    else:
        query = current_user.albums()
    query = query.order_by(Album.end_date.desc())
    return {a.url_title: a for a in query}


def _get_album_date_range(album_id: int) -> Tuple[datetime, datetime]:
    creation_dates = tuple(
        item.metadata().get("creationTime") for item in get_media(album_id) if item.metadata().get("creationTime")
    )
    start_date = min(creation_dates)
    end_date = max(creation_dates)
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    return (datetime.strptime(start_date, fmt), datetime.strptime(end_date, fmt))


def cache_albums(refresh_thumbnails=False, refresh_dates=False):
    album_manager = GPhotosAlbum(service)
    current_ids = list()
    for a in album_manager.list():
        album = Album.query.filter_by(gphotos_id=a.get("id")).first()
        if not album:
            album = Album()
        album.gphotos_id = a.get("id")
        if not album.end_date or refresh_dates:
            start_date, end_date = _get_album_date_range(album.gphotos_id)
            album.start_date = start_date
            album.end_date = end_date
        current_ids.append(a.get("id"))
        album.title = a.get("title")
        album.url_title = normalize_for_url(a.get("title"))
        album.items_count = a.get("mediaItemsCount")
        db.session.add(album)
        thumbnail = os.path.join(app.config["ALBUM_THUMB_PATH"], a.get("id") + ".jpg")
        if not os.path.exists(thumbnail) or refresh_thumbnails:
            urllib.request.urlretrieve(
                a.get("coverPhotoBaseUrl") + "=w300-h200-c",
                os.path.join(app.config["ALBUM_THUMB_PATH"], a.get("id") + ".jpg"),
            )

    # delete from db albums no longer in google photos
    stmt = delete(Album).where(Album.gphotos_id.notin_(current_ids)).execution_options(synchronize_session="fetch")
    db.session.execute(stmt)
    db.session.commit()


@cache.memoize()
def get_media(album_id):
    media_manager = Media(service)
    album_media_list = list(MediaItem(m) for m in media_manager.search_album(album_id))
    return album_media_list

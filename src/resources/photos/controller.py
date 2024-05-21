from src.resources.photos.models import GetAlbumsResponse, Album, GetItemsResponse, MediaItem
from src.resources.photos.services import AlbumsService, MediaItemsService


class GooglePhotosController:
    def __init__(self, client):
        self.albums_service = AlbumsService(client)
        self.media_items_service = MediaItemsService(client)

    def get_albums(self):
        albums = list(self.albums_service.list())
        return GetAlbumsResponse(albums=[Album.parse_obj(album) for album in albums], total=len(albums))

    def get_favorite_items_from_album(self, album_id: str):
        all_favorite_items = list(self.media_items_service.get_favorite_items())
        album_item_ids = [item['id'] for item in self.media_items_service.get_album_items(album_id)]
        favorite_items_from_album = [item for item in all_favorite_items if item['id'] in album_item_ids]

        return GetItemsResponse(
            mediaItems=[MediaItem.parse_obj(item) for item in favorite_items_from_album],
            total=len(favorite_items_from_album)
        )
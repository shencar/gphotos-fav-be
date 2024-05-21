from functools import cached_property

from src.resources.photos.clients import GooglePhotosClient


def page_iterator(data_field):
    def decorator(func, *args, **kwargs):
        def wrapper(self, *args, **kwargs):
            page_token = kwargs.pop('page_token', None)
            while True:
                response = func(self, *args, **kwargs, page_token=page_token)
                yield from response[data_field]
                page_token = response.get('nextPageToken')
                if not page_token:
                    break

        return wrapper

    return decorator


class BaseService:
    DEFAULT_PAGE_SIZE = 50

    def __init__(self, client: GooglePhotosClient):
        self.client = client

    def __hash__(self):
        return hash(self.client)


class AlbumsService(BaseService):

    @cached_property
    def _service(self):
        return self.client._client.albums()

    @page_iterator(data_field='albums')
    def list(self, page_token=None):
        return self._service.list(pageToken=page_token, pageSize=self.DEFAULT_PAGE_SIZE).execute()

    def get_album(self, album_id):
        return self._service.get(albumId=album_id).execute()


class MediaItemsService(BaseService):
    DEFAULT_PAGE_SIZE = 100

    @cached_property
    def _service(self):
        return self.client._client.mediaItems()

    @page_iterator(data_field='mediaItems')
    def get_favorite_items(self, page_token=None):
        return self._service.search(body={
            "filters": {"featureFilter": {"includedFeatures": ["FAVORITES"]}},
            "pageSize": self.DEFAULT_PAGE_SIZE,
            "pageToken": page_token,
        }).execute()

    @page_iterator(data_field='mediaItems')
    def get_album_items(self, album_id, page_token=None):
        return self._service.search(body={
            'albumId': album_id,
            "pageSize": self.DEFAULT_PAGE_SIZE,
            "pageToken": page_token,
        }).execute()

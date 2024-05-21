from typing import List

from pydantic import BaseModel, validator, field_validator


class Album(BaseModel):
    id: str
    title: str
    productUrl: str
    isWriteable: bool = True
    mediaItemsCount: int = 0
    coverPhotoBaseUrl: str = ''
    coverPhotoMediaItemId: str = ''


class GetAlbumsResponse(BaseModel):
    albums: List[Album] = []
    total: int = 0


class MediaMetadata(BaseModel):
    creationTime: str
    width: str
    height: str
    photo: dict = {}


class MediaItem(BaseModel):
    id: str
    productUrl: str
    baseUrl: str
    mimeType: str
    mediaMetadata: MediaMetadata
    filename: str


class GetItemsResponse(BaseModel):
    mediaItems: List[MediaItem] = []
    total: int = 0

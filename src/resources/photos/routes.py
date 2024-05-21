from fastapi import APIRouter, Depends, Request

from src.resources.authentication.dependencies import auth_required
from src.resources.photos.controller import GooglePhotosController
from src.resources.photos.dependencies import init_controller
from src.resources.photos.models import GetAlbumsResponse, GetItemsResponse

router = APIRouter()


@router.get('/test')
async def test_api_request(request: Request):
    return ''


@router.get('/albums')
@router.get('/')
async def get_albums(
        request: Request,
        user=Depends(auth_required),
        controller: GooglePhotosController = Depends(init_controller)
) -> GetAlbumsResponse:
    return controller.get_albums()


@router.get('/albums/{album_id}/favorites')
async def get_favorite_items_from_album(
        request: Request,
        album_id: str,
        user=Depends(auth_required),
        controller: GooglePhotosController = Depends(init_controller)
) -> GetItemsResponse:
    return controller.get_favorite_items_from_album(album_id)

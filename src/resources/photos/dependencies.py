from fastapi import Request

from src.resources.photos.clients import GooglePhotosClient
from src.resources.photos.controller import GooglePhotosController


def init_controller(request: Request):
    client = GooglePhotosClient(request.session['credentials'])
    return GooglePhotosController(client)

import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from resources.authentication.routes import router as authentication_router
from resources.photos.routes import router as photos_router

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))


def setup_resources(app):
    app.include_router(authentication_router)
    app.include_router(photos_router)


def setup_app(version):
    logging.info(f'Setting up Ogen DB API v{version}')

    _app = FastAPI(version=version)
    origins = ["*"]

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.add_middleware(
        SessionMiddleware,
        secret_key=''
    )

    # _app.add_middleware(HTTPSRedirectMiddleware)

    setup_resources(_app)

    return _app

app = setup_app(os.getenv('APP_VERSION', '0.0.1'))

@app.get('/version')
async def version():
    return {
        'version': app.version
    }

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    uvicorn.run('server:app', host='0.0.0.0', port=4000)
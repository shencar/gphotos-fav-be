import urllib

import google
import google_auth_oauthlib
from fastapi import APIRouter, Request, HTTPException
from starlette import status
from starlette.responses import RedirectResponse
import requests

router = APIRouter(prefix='/auth')

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "/home/bs/work/tasks/Tasks/client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly",
          "https://www.googleapis.com/auth/photoslibrary.appendonly",
          "https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata",
          "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata",
          "https://www.googleapis.com/auth/photoslibrary.sharing",
          "https://www.googleapis.com/auth/photoslibrary"]


@router.get("/authorize")
async def authorize(request: Request):
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = request.url_for("callback")

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )

    # Store the state so the callback can verify the auth server response.
    request.session["state"] = state

    return RedirectResponse(authorization_url)


@router.get("/callback")
async def callback(request: Request):
    # Specify the state when creating the flow in the callback so that it can be
    # verified in the authorization server response.
    state = request.session["state"]

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = request.url_for("callback")

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    request.session["credentials"] = credentials_to_dict(credentials)

    original_url = request.session.get('original_url', '/')
    if original_url:
        del request.session["original_url"]
        response = RedirectResponse(original_url)
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No original URL found in the session",
        )


@router.get("/revoke")
def revoke(request: Request):
    if "credentials" not in request.session:
        return (
                'You need to <a href="/authorize">authorize</a> before '
                + "testing the code to revoke credentials."
        )

    credentials = google.oauth2.credentials.Credentials(**request.session["credentials"])

    revoke = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    clear_credentials(request)

    status_code = getattr(revoke, "status_code")
    if status_code == 200:
        return "Credentials successfully revoked."
    else:
        return "An error occurred."

@router.get("/clear")
def clear_credentials(request: Request):
    if "credentials" in request.session:
        del request.session["credentials"]
    return "Credentials have been cleared.<br><br>"


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

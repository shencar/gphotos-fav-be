from functools import wraps

from fastapi import HTTPException, Request
from starlette import status


async def auth_required(request: Request):
    # Check if the user is authenticated
    is_authenticated = request.session.get("credentials", False)

    if is_authenticated:
        # User is authenticated, return None to allow the route handler to proceed
        return
    else:
        # User is not authenticated, save the original URL in the session
        request.session["original_url"] = str(request.url)

        # Redirect the user to the authentication flow
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Redirecting to authentication flow",
            headers={"Location": str(request.url_for('authorize'))},
        )

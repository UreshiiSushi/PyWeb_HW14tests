from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import UserDb
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=UserDb,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves a current user from DB by access token.

    :param current_user: The user with specified  access token.
    :type current_user: User
    :return: The specified user or error message.
    :rtype: User | json
    """
    return current_user


@router.patch(
    "/avatar",
    response_model=UserDb,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Updates an avatar for current user.

    :param file: The image for a new avatar.
    :type file: UploadFile
    :param current_user: The user with specified  access token.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The specified user or error message.
    :rtype: User | json
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    r = cloudinary.uploader.upload(
        file.file, public_id=f"NotesApp/{current_user.username}", overwrite=True
    )
    src_url = cloudinary.CloudinaryImage(f"NotesApp/{current_user.username}").build_url(
        width=250, height=250, crop="fill", version=r.get("version")
    )
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
from libgravatar import Gravatar
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a single user with the specified email.

    :param email: The email to retrieve user for.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The single user with the specified email.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a single user with the specified credentials.

    :param body: The credentials to create user for.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The single user with the specified credentials.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates a token for a single user with the specified credentials.

    :param user: The single user with the specified credentials.
    :type user: User
    :param token: Token to update.
    :type token: str
    :param db: The database session.
    :type db: Session
    :return: None to return.
    :rtype: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Procedure for confirming email upon registration.

    :param email: The email for confirmation.
    :type user: str
    :param db: The database session.
    :type db: Session
    :return: None to return.
    :rtype: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    Updates an avatar for single user with the specified email.

    :param email: The email to find user for.
    :type email: str
    :param url: Link pointing to avatar.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The single user with updated avatar.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user

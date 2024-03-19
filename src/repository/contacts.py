from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from datetime import date, datetime, timedelta
from src.schemas import ContactEmail, ContactModel, ResponseContactModel


async def create_contact(
    contact: ContactModel, user: User, db: Session
) -> ContactModel:
    """
    Creates a new contact for specific user.

    :param contact: contact details.
    :type contact: ContactModel
    :param user: The user to create the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contsct.
    :rtype: ContactModel
    """
    new_contact = Contact(
        name=contact.name,
        lastname=contact.lastname,
        email=contact.email,
        phone=contact.phone,
        born_date=contact.born_date,
        description=contact.description,
        user=user,
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


async def get_contacts(user: User, db: Session) -> List[ResponseContactModel]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The list of found contacts.
    :rtype: List[ResponseContactModel]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).all()


async def get_contact(contact_id: int, user: User, db: Session) -> ContactModel:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The specified contact.
    :rtype: ContactModel
    """
    return (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )


async def update_contact(
    contact_id: int,
    user: User,
    db: Session,
    name: str,
    lastname: str,
    email: str,
    phone: str,
    born_date: str,
    description: str,
) -> ContactModel:
    """
    Update a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param user: The user to update contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :param name: The new contact's name.
    :type name: str
    :param lastname: The new contact's lastname.
    :type lastname: str
    :param email: The new contact's email.
    :type email: str
    :param phone: The new contact's phone.
    :type phone: str
    :param born_date: The new contact's born_date.
    :type born_date: str
    :param description: The new contact's description.
    :type description: str
    :return: The updated contact.
    :rtype: ContactModel
    """
    target_contact = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    if not target_contact:
        return
    if name:
        target_contact.name = name
    if lastname:
        target_contact.lastname = lastname
    if email:
        target_contact.email = email
    if phone:
        target_contact.phone = phone
    if born_date:
        target_contact.born_date = born_date
    if description:
        target_contact.description = description

    db.commit()
    return target_contact


async def delete_contact(contact_id, user: User, db: Session) -> Contact | None:
    """
    Delete a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :param user: The user to delete contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The deleted contact.
    :rtype: ContactModel
    """
    item = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    if item:
        db.delete(item)
        db.commit()
        return item


async def search_data(
    user: User, db: Session, name: str, lastname: str, email: str
) -> ContactModel | None:
    """
    Search a single contact with the specified name, lastname or email for a specific user.

    :param user: The user to find contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :param name: The contact's name.
    :type name: str
    :param lastname: The contact's lastname.
    :type lastname: str
    :param email: The contact's email.
    :type email: str
    :return: The found contact.
    :rtype: ContactModel
    """

    if name:
        return (
            db.query(Contact)
            .filter(and_(Contact.name == name, Contact.user_id == user.id))
            .first()
        )
    if lastname:
        return (
            db.query(Contact)
            .filter(and_(Contact.lastname == lastname, Contact.user_id == user.id))
            .first()
        )
    if email:
        return (
            db.query(Contact)
            .filter(and_(Contact.email == email, Contact.user_id == user.id))
            .first()
        )


async def birthday_to_week(user: User, db: Session) -> List[ContactModel] | None:
    """
    Search for birthday contacts in the coming week.

    :param user: The user to find contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The list of found contacts.
    :rtype: List[ContactModel]
    """
    users = db.query(Contact).filter(Contact.user_id == user.id).all()
    if not users:
        return
    week = date.today() + timedelta(days=6)
    happy_users = []
    for user in users:
        bday = datetime(
            date.today().year,
            user.born_date.month,
            user.born_date.day,
        ).date()

        if date.today() <= bday <= week:
            happy_users.append(user)

    return happy_users

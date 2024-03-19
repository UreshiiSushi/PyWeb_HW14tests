import datetime
import unittest
from unittest.mock import MagicMock
from sqlalchemy import and_
from sqlalchemy.orm import Session


from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    delete_contact,
    update_contact,
    search_data,
    birthday_to_week,
)
from src.database.models import Contact, User


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact_id = 1

    async def test_get_contacts(self):
        contacts = [
            Contact(),
        ]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
            phone="3800502128506",
            born_date="1988-01-12",
            description="Just friend",
        )

        result = await create_contact(contact=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.born_date, body.born_date)
        self.assertEqual(result.description, body.description)

        self.assertTrue(hasattr(result, "id"))

    async def test_delete_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await delete_contact(
            contact_id=self.contact_id, user=self.user, db=self.session
        )
        self.assertEqual(result, contact)

    async def test_delete_contact_not_found(self):

        self.session.query().filter().first.return_value = None
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        contact = ContactModel(
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
            phone="3800502128506",
            born_date="1988-01-12",
            description="Just friend",
        )

        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(
            contact_id=1,
            user=self.user,
            db=self.session,
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
            phone="3800502128506",
            born_date="1988-01-12",
            description="Just strange friend",
        )
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        contact = ContactModel(
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
            phone="3800502128506",
            born_date="1988-01-12",
            description="Just friend",
        )

        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(
            contact_id=1,
            user=self.user,
            db=self.session,
            name="Deira",
            lastname="Hadid",
            email="dhadid@gmail.com",
            phone="3800502128506",
            born_date="1988-01-12",
            description="Just strange friend",
        )
        self.assertIsNone(result)

    async def test_search_contact_found_name(self):
        contact = ContactModel(
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
            phone="3800502128506",
            born_date="1988-01-12",
            description="Just friend",
        )
        self.session.query().filter().first.return_value = contact
        result = await search_data(
            user=self.user,
            db=self.session,
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
        )
        self.assertEqual(result, contact)

    async def test_search_contact_found_lastname(self):
        contact = ContactModel(
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
            phone="3800502128506",
            born_date="1988-01-12",
            description="Just friend",
        )
        self.session.query().filter().first.return_value = contact
        result = await search_data(
            user=self.user,
            db=self.session,
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
        )
        self.assertEqual(result, contact)

    async def test_search_contact_found_email(self):
        contact = ContactModel(
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
            phone="3800502128506",
            born_date="1988-01-12",
            description="Just friend",
        )
        self.session.query().filter().first.return_value = contact
        result = await search_data(
            user=self.user,
            db=self.session,
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
        )
        self.assertEqual(result, contact)

    async def test_search_contact_found_all_together(self):
        contact = ContactModel(
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
            phone="3800502128506",
            born_date="1988-01-12",
            description="Just friend",
        )
        self.session.query().filter().first.return_value = contact
        result = await search_data(
            user=self.user,
            db=self.session,
            name="Bill",
            lastname="Fork",
            email="fork_bill@gmail.com",
        )
        self.assertEqual(result, contact)

    async def test_search_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await search_data(
            user=self.user,
            db=self.session,
            name="Brenda",
            lastname="Gerard",
            email="breger@gmail.com",
        )
        self.assertIsNone(result)

    async def test_birthday_to_week_found(self):
        contacts = [
            ContactModel(
                name="Bill",
                lastname="Fork",
                email="fork_bill@gmail.com",
                phone="3800502128506",
                born_date=datetime.date.today() + datetime.timedelta(days=3),
                description="Just friend",
            ),
        ]
        self.session.query().filter().all.return_value = contacts
        result = await birthday_to_week(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_birthday_to_week_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await birthday_to_week(user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

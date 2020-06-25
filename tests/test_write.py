"""TEST WRITE
Test write actions (create, update, delete)
"""

# # Native # #
from datetime import datetime
from random import randint

# # Project # #
from people_api.models import *
from people_api.repositories import PeopleRepository

# # Installed # #
import pydantic
from freezegun import freeze_time
from dateutil.relativedelta import relativedelta
from fastapi import status as statuscode

# # Package # #
from .base import BaseTest
from .utils import *


class PersonAsCreate(PersonCreate):
    """This model is used to convert PersonRead to PersonCreate,
     to compare the responses returned by the API with the create objects sent"""
    class Config(PersonCreate.Config):
        extra = pydantic.Extra.ignore


class TestCreate(BaseTest):
    def test_create_person(self):
        """Create a person.
        Should return the person"""
        create = get_person_create().dict()

        response = self.create_person(create)
        response_as_create = PersonAsCreate(**response.json())
        assert response_as_create.dict() == create

    def test_create_person_assert_birth_age(self):
        """Create a person.
        Should create the person with the given date of birth and calculate its age"""
        expected_age = randint(5, 25)
        today = datetime.now().date()
        birth = today - relativedelta(years=expected_age)
        create = get_person_create(birth=birth).dict()

        response = self.create_person(create)
        response_as_read = PersonRead(**response.json())

        assert response_as_read.birth == birth
        assert response_as_read.age == expected_age

    def test_create_person_without_birth(self):
        """Create a person without date of birth.
        Should return the person without birth nor age"""
        create = get_person_create(birth=None).dict()

        response = self.create_person(create)
        response_as_read = PersonRead(**response.json())

        assert response_as_read.birth is None
        assert response_as_read.age is None

    def test_timestamp_created_updated(self):
        """Create a person and assert the created and updated timestamp fields.
        The creation is performed against the PeopleRepository,
        since mocking the time would not work as the testing API runs on another process"""
        iso_timestamp = "2020-01-01T00:00:00+00:00"
        expected_timestamp = int(datetime.fromisoformat(iso_timestamp).timestamp())

        with freeze_time(iso_timestamp):
            create = get_person_create()
            result = PeopleRepository.create(create)

        assert result.created == result.updated
        assert result.created == expected_timestamp


class TestDelete(BaseTest):
    def test_delete_person(self):
        """Delete a person.
        Then get it. Should end returning 404 not found"""
        person = get_existing_person()

        self.delete_person(person.person_id)
        self.get_person(person.person_id, statuscode=statuscode.HTTP_404_NOT_FOUND)

    def test_delete_nonexisting_person(self):
        """Delete a person that does not exist.
        Should return not found 404 error and the identifier"""
        person_id = get_uuid()

        response = self.delete_person(person_id, statuscode=statuscode.HTTP_404_NOT_FOUND)
        assert response.json()["identifier"] == person_id


class TestUpdate(BaseTest):
    def test_update_person_single_attribute(self):
        """Update the name of a person.
        Then get it. Should return the person with its name updated"""
        person = get_existing_person()

        new_name = get_uuid()
        update = PersonUpdate(name=new_name)
        self.update_person(person.person_id, update.dict())

        read = PersonRead(**self.get_person(person.person_id).json())
        assert read.name == new_name
        assert read.dict() == {**person.dict(), "name": new_name, "updated": read.updated}

    def test_update_nonexisting_person(self):
        """Update the name of a person that does not exist.
        Should return not found 404 error and the identifier"""
        person_id = get_uuid()
        update = PersonUpdate(name=get_uuid())

        response = self.update_person(person_id, update.dict(), statuscode=statuscode.HTTP_404_NOT_FOUND)
        assert response.json()["identifier"] == person_id

    def test_update_person_none_attributes(self):
        """Update a person sending an empty object.
        Should return validation error 422"""
        person = get_existing_person()
        self.update_person(person.person_id, {}, statuscode=statuscode.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_update_person_extra_attributes(self):
        """Update a person sending unknown attributes.
        Should return validation error 422"""
        person = get_existing_person()
        self.update_person(person.person_id, {"foo": "bar"}, statuscode=statuscode.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_timestamp_updated(self):
        """Update a person and assert the updated timestamp.
        The update is performed against the PeopleRepository,
        since mocking the time would not work as the testing API runs on another process"""
        iso_timestamp = "2020-04-01T00:00:00+00:00"
        expected_timestamp = int(datetime.fromisoformat(iso_timestamp).timestamp())
        person = get_existing_person()

        with freeze_time(iso_timestamp):
            update = PersonUpdate(name=get_uuid())
            PeopleRepository.update(person_id=person.person_id, update=update)

        read_response = self.get_person(person.person_id)
        read = PersonRead(**read_response.json())

        assert read.updated == expected_timestamp
        assert read.updated != read.created
        assert read.created == person.created

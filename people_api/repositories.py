"""REPOSITORIES
Methods to interact with the database
"""

# # Package # #
from .models import *
from .exceptions import *
from .database import collection
from .utils import get_time, get_uuid

__all__ = ("PeopleRepository",)


class PeopleRepository:
    @staticmethod
    def get(person_id: str) -> PersonRead:
        """Retrieve a single Person by its unique id"""
        document = collection.find_one({"_id": person_id})
        if not document:
            raise PersonNotFound(person_id)
        return PersonRead(**document)

    @staticmethod
    def list() -> PeopleRead:
        """Retrieve all the available persons"""
        cursor = collection.find()
        return [PersonRead(**document) for document in cursor]

    @staticmethod
    def create(create: PersonCreate) -> PersonRead:
        """Create a person and return its Read object"""
        document = create.dict()
        document["created"] = document["updated"] = get_time()
        document["_id"] = get_uuid()
        # The time and id could be inserted as a model's Field default factory,
        # but would require having another model for Repository only to implement it

        result = collection.insert_one(document)
        assert result.acknowledged

        return PeopleRepository.get(result.inserted_id)

    @staticmethod
    def update(person_id: str, update: PersonUpdate):
        """Update a person by giving only the fields to update"""
        document = update.dict()
        document["updated"] = get_time()
        
        result = collection.update_one({"_id": person_id}, {"$set": document})
        if not result.modified_count:
            raise PersonNotFound(person_id)

    @staticmethod
    def delete(person_id: str):
        """Delete a person given its unique id"""
        result = collection.delete_one({"_id": person_id})
        if not result.deleted_count:
            raise PersonNotFound(person_id)

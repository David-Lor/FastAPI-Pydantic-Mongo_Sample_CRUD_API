"""MODELS - PERSON - CREATE
Person Create model. Inherits from PersonUpdate, but all the required fields must be re-defined
"""

# # Package # #
from .person_update import PersonUpdate
from .person_address import Address
from .fields import PersonFields

__all__ = ("PersonCreate",)


class PersonCreate(PersonUpdate):
    """Body of Person POST requests"""
    name: str = PersonFields.name
    address: Address = PersonFields.address
    # Birth remains Optional, so is not required to re-declare

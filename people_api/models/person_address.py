"""MODELS - PERSON ADDRESS
The address of a person is part of the Person model
"""

# # Package # #
from .common import BaseModel
from .fields import AddressFields

__all__ = ("Address",)


class Address(BaseModel):
    """The address information of a person"""
    street: str = AddressFields.street
    city: str = AddressFields.city
    state: str = AddressFields.state
    zip_code: str = AddressFields.zip_code

"""MODELS - PERSON - UPDATE
Person Update model. All attributes are set as Optional, as we use the PATCH method for update
(in which only the attributes to change are sent on request body)
"""

# # Native # #
from datetime import date
from typing import Optional
from contextlib import suppress

# # Package # #
from .common import BaseModel
from .fields import PersonFields
from .person_address import Address

__all__ = ("PersonUpdate",)


class PersonUpdate(BaseModel):
    """Body of Person PATCH requests"""
    name: Optional[str] = PersonFields.name
    address: Optional[Address] = PersonFields.address_update
    birth: Optional[date] = PersonFields.birth

    def dict(self, **kwargs):
        # The "birth" field must be converted to string (isoformat) when exporting to dict (for Mongo)
        # TODO Better way to do this? (automatic conversion can be done with Config.json_encoders, but not available for dict
        d = super().dict(**kwargs)
        with suppress(KeyError):
            d["birth"] = d.pop("birth").isoformat()
        return d

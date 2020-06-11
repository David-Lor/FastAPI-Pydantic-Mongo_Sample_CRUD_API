"""EXCEPTIONS
Custom exceptions with responses
"""

# # Installed # #
from fastapi.responses import JSONResponse
from fastapi import status as statuscode

__all__ = (
    "EntityError", "NotFound",
    "PersonNotFound"
)


class EntityError(Exception):
    """Base errors for entities, uniquely identified"""
    message = "Entity error"
    code = statuscode.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, identifier):
        self.id = identifier

    @property
    def response(self):
        return JSONResponse(
            content={
                "id": self.id,
                "message": self.message
            },
            status_code=self.code
        )


class NotFound(EntityError):
    """The entity does not exist"""
    message = "The entity does not exist"
    code = statuscode.HTTP_404_NOT_FOUND


class PersonNotFound(NotFound):
    """The Person does not exist"""
    message = "The person does not exist"

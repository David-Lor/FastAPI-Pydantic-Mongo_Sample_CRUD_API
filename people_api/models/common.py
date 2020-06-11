"""MODELS - COMMON
Common variables and base classes for the models
"""

# # Installed # #
import pydantic

__all__ = ("BaseModel",)


class BaseModel(pydantic.BaseModel):
    """All data models inherit from this class"""

    @pydantic.root_validator(pre=True)
    def _min_properties(cls, data):
        """At least one property is required"""
        if not data:
            raise ValueError("At least one property is required")
        return data

    def dict(self, include_nulls=False, **kwargs):
        """Override the super dict method by removing null keys from the dict, unless include_nulls=True"""
        kwargs["exclude_none"] = not include_nulls
        return super().dict(**kwargs)

    class Config:
        extra = pydantic.Extra.forbid  # forbid sending additional fields/properties
        anystr_strip_whitespace = True  # strip whitespaces from strings

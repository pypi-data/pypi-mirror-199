from functools import partialmethod
from typing import ClassVar

import attrs
from pydantic import root_validator, validate_arguments


# noinspection PyUnresolvedReferences, PyMethodParameters
class Fields(validate_arguments(attrs.field).model):
    """
    Helper class for creating attrs fields. https://attrs.org

    Notes
    -----
    This class is a Pydantic model created from the signature of :meth:`attrs.field`.
    """

    class Config:
        fields = {k: {"exclude": True} for k in ("frozen", "args", "kwargs")}

    setters: ClassVar = attrs.setters
    validators: ClassVar = attrs.validators

    frozen: bool = False

    @root_validator
    def validate(cls, values):
        if values["frozen"]:
            if values["on_setattr"] is not None:
                values["on_setattr"] = cls.setters.pipe(
                    cls.setters.frozen, values["on_setattr"]
                )
            else:
                values["on_setattr"] = cls.setters.frozen

        return values

    @classmethod
    def field(cls, *, frozen: bool = False, **kwargs):
        return attrs.field(**cls.parse_obj(dict(kwargs, frozen=frozen)).dict())

    attr = classmethod(partialmethod(field, init=False))

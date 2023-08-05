from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union, get_origin, cast

from pydantic import BaseModel as OriginalBaseModel
from pydantic import create_model, root_validator
from pydantic.fields import ModelField
from pydantic.json import ENCODERS_BY_TYPE
from pydantic.typing import is_none_type

__all__ = "BaseModel", "Option"
_T = TypeVar("_T")
_V = TypeVar("_V")


def _is_option_type(type_: Type[Any]) -> bool:
    if is_none_type(type_):
        return False
    origin = get_origin(type_)
    if is_none_type(origin):
        return False
    return origin is Option


def _get_default_fields(schema: Dict[str, Any]) -> Dict[str, Any]:
    properties = cast(dict, schema.get("properties", {}))
    return {
        k: properties[k]["default"] for k in properties if "default" in properties[k]
    }


def _get_required_option_fields(
    annotations: Dict[str, Any], schema: Dict[str, Any]
) -> Dict[str, "Option"]:
    properties = cast(dict, schema.get("properties", {}))
    return {
        k: Option()
        for k in properties
        if k in schema.get("required", [])
        or "default" not in properties[k]
        and _is_option_type(annotations[k])
    }


def _create_result_model(field_name: str, value: Any, type_: Type[Any]) -> "BaseModel":
    return create_model(
        "ResultModel",
        __base__=BaseModel,
        **{
            field_name: (
                type_,
                value,
            )
        },
    )()


class Option(Generic[_T]):
    """Type Option in order to correctly handle optional value."""

    __value: Optional[_T]

    def __init__(self, value: Optional[_T] = None) -> None:
        self.__value = value

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "%s(%s)" % (
            self.__class__.__name__,
            repr(self.__value),
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, field: ModelField) -> "Option[_T]":
        result_type = field.outer_type_.__args__[0]
        field_name = field.name.removeprefix("_").removesuffix("_")
        if isinstance(v, cls):
            if v.is_none:
                return v
            _model = _create_result_model(field_name, v.unwrap(), result_type)
            return cls(getattr(_model, field_name))
        if v is None:
            return cls(v)
        _model = _create_result_model(field_name, v, result_type)
        return cls(getattr(_model, field_name))

    @property
    def is_none(self) -> bool:
        """Return True if value is None."""
        return self.__value is None

    def unwrap(self, *, error_msg: str = None) -> _T:
        """Unwrap the optional value if it's not None, otherwise a
        ValueError will be raised with the appropriate error_msg.
        """
        if self.__value is None:
            raise ValueError(error_msg if error_msg is not None else "Value is None.")
        return self.__value

    def unwrap_or(self, variant: _V, /) -> Union[_T, _V]:
        """Unwrap the optional value if it's not None,
        otherwise it will return the variant you passed.
        """
        if variant is None:
            raise TypeError("Variant should not be type 'NoneType'.")
        return self.__value if self.__value is not None else variant


class BaseModel(OriginalBaseModel):
    @root_validator(pre=True)
    @classmethod
    def _root_validate_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        model_schema = cls.schema()
        fields = _get_default_fields(model_schema)
        fields.update(_get_required_option_fields(cls.__annotations__, model_schema))
        fields.update(values)
        return {
            field: Option(value)
            if _is_option_type(cls.__annotations__.get(field, None))
            and not isinstance(value, Option)
            else value
            for field, value in fields.items()
        }


ENCODERS_BY_TYPE[Option] = lambda v: None if v.is_none else v.unwrap()

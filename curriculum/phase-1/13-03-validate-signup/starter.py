from typing import Literal, TypedDict, Union


class SignupForm(TypedDict):
    username: str
    email: str
    password: str
    confirm_password: str


Field = Literal["username", "email", "password", "confirm_password"]


class FieldError(TypedDict):
    field: Field
    message: str


class Valid(TypedDict):
    valid: Literal[True]


class Invalid(TypedDict):
    valid: Literal[False]
    errors: list[FieldError]


ValidationResult = Union[Valid, Invalid]


def validate_signup(form: SignupForm) -> ValidationResult:
    """Return {"valid": True} or {"valid": False, "errors": [...]} with the first broken rule of every field, in field order."""
    raise NotImplementedError

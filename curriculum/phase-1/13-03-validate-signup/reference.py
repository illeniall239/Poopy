# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from string import ascii_letters, digits
from typing import Literal, Optional, TypedDict, Union


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


def check_username(raw: str) -> Optional[str]:
    username = raw.strip()
    if username == "":
        return "Username is required"
    if len(username) < 3 or len(username) > 20:
        return "Username must be 3 to 20 characters"
    for ch in username:
        if ch not in ascii_letters and ch not in digits and ch != "_":
            return "Username may only contain letters, digits and underscores"
    return None


def check_email(raw: str) -> Optional[str]:
    email = raw.strip()
    if email == "":
        return "Email is required"
    parts = email.split("@")
    valid = " " not in email and len(parts) == 2 and len(parts[0]) > 0 and "." in parts[1][1:-1]
    return None if valid else "Email is not valid"


def check_password(password: str) -> Optional[str]:
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not any(ch in digits for ch in password):
        return "Password must contain a digit"
    if not any(ch in ascii_letters for ch in password):
        return "Password must contain a letter"
    return None


def validate_signup(form: SignupForm) -> ValidationResult:
    errors: list[FieldError] = []

    def add(field: Field, message: Optional[str]) -> None:
        if message is not None:
            errors.append({"field": field, "message": message})

    add("username", check_username(form["username"]))
    add("email", check_email(form["email"]))
    add("password", check_password(form["password"]))
    add("confirm_password", None if form["confirm_password"] == form["password"] else "Passwords do not match")
    return {"valid": True} if len(errors) == 0 else {"valid": False, "errors": errors}

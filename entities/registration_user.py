from pydantic import BaseModel
from entities.roles import Roles
import pytest

class RegistrationUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[Roles]
    banned: bool | None = None
    verified: bool | None = None
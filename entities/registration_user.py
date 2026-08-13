from pydantic import BaseModel, Field
from entities.roles import Roles

class RegistrationUser(BaseModel):
    email: str = Field(pattern=r".+@.+") #Field доп ограничение к полю #в скобках регулярное выражение
    fullName: str
    password: str = Field(min_length=9)
    passwordRepeat: str
    roles: list[Roles]
    banned: bool | None = None
    verified: bool | None = None
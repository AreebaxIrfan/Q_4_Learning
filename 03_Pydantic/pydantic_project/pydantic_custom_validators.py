from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import List


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr
    addresses: List[Address]

    @field_validator("name")
    def name_must_be_at_least_two_chars(cls, v):
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return v

    @field_validator("email")
    def email_must_be_company_domain(cls, v):
        if not v.endswith("@mycompany.com"):
            raise ValueError("Email must be a company email (@mycompany.com)")
        return v


# Test with invalid data
try:
    user = UserWithAddress(
        id=1,
        name="Z",
        email="user@gmail.com",  # Invalid domain
        addresses=[
            {"street": "456 Elm St", "city": "Austin", "zip_code": "ABC123"}  # Invalid zip
        ],
    )
except ValidationError as e:
    print(e)
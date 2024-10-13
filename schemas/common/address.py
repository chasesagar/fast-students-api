from pydantic import BaseModel
from typing_extensions import Optional


class AddressSchema(BaseModel):
    """
    Address pydantic schema
    """
    house_number: Optional[str]
    street: str
    city: str
    state: str
    state_code: Optional[str]
    zip: str
    postal_code: Optional[str]
    country: str
    country_code: Optional[str]
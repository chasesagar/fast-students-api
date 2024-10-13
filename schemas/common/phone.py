from pydantic import BaseModel


class PhoneSchema(BaseModel):
    """
    Schema for phone number
    """

    phone: str
    country_code: str

from pydantic import BaseModel


class LocationSchema(BaseModel):
    """
    Schema representing location pydantic model
    """
    latitude: float
    longitude: float
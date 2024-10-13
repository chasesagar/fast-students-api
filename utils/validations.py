from typing import Optional

from pydantic import ValidationError

def validate_age(value: int) -> Optional[int]:
    """
    Validate the age value.

    Args:
        value (int): The age value to validate.

    Returns:
        int: The validated age value.

    Raises:
        ValueError: If the age value is not between 3 and 20 (inclusive).
    """

    if value is not None and (value < 3 or value > 20):
        raise ValueError("Age must be between 3 and 20.")

    return value

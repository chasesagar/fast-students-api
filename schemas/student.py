from typing import Optional, List

from pydantic import BaseModel, field_validator

from enums.gender_enum import GenderEnum
from enums.student.grade_enum import StudentGradeEnum
from schemas.common.address import AddressSchema
from schemas.common.location import LocationSchema
from schemas.common.phone import PhoneSchema
from utils.validations import validate_age


class _StudentAddressSchema(BaseModel):
    """
    Schema for representing a student address
    """
    label: str
    address: AddressSchema
    location: LocationSchema
    am_preferred: bool
    am_preferred: bool


class _StudentParentSchema(BaseModel):
    """
    Schema for representing a student parent
    """
    parent_id: Optional[str] = None
    first_name: str
    last_name: str
    relation: Optional[str]
    email: Optional[str] = None
    phone: Optional[PhoneSchema] = None


class _StudentSpecialNeedsSchema(BaseModel):
    """
    Schema for representing a student special needs
    """
    has_special_needs: bool
    special_needs_type: Optional[str]

class _StudentNotesSchema(BaseModel):
    """
    Schema for representing a student notes
    """
    school_notes: Optional[str]
    driver_notes: Optional[str]


class _BaseStudentSchema(BaseModel):
    """
    Base pydantic schema for student
    """
    school_id: str
    first_name: str
    last_name: str
    gender: GenderEnum
    grade: StudentGradeEnum
    birthdate: str
    special_needs: _StudentSpecialNeedsSchema
    age: int
    email: Optional[str] = None
    phone: Optional[PhoneSchema] = None
    addresses: List[Optional[_StudentAddressSchema]] = []
    parents: List[_StudentParentSchema]
    notes: Optional[_StudentNotesSchema] = None

    @field_validator('age')
    def validate_age(cls, v):
        return validate_age(value=v)


class CreateStudentSchema(_BaseStudentSchema):
    """
    Schema for creating a new student
    """
    pass


class StudentSchema(_BaseStudentSchema):
    """
    Schema for representing a student
    """
    student_id: str

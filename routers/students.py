from typing import Optional

from fastapi import APIRouter

from schemas.student import CreateStudentSchema

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_students(school_id: str, org_id: Optional[str] = None):
    return {"message": f"Get students for school {school_id}"}


@router.post("/")
async def create_student(student: CreateStudentSchema):
    print(student)
    return student.model_dump()


@router.get("/{student_id}")
async def get_student(student_id: int):
    return {"message": f"Get student {student_id}"}


@router.put("/{student_id}")
async def update_student(student_id: int):
    return {"message": f"Update student {student_id}"}


@router.delete("/{student_id}")
async def delete_student(student_id: int):
    return {"message": f"Delete student {student_id}"}

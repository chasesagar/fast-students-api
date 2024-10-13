from fastapi import APIRouter

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_students():
    return {"message": "Get students"}


@router.post("/")
async def create_student():
    return {"message": "Create student"}


@router.get("/{student_id}")
async def get_student(student_id: int):
    return {"message": f"Get student {student_id}"}


@router.put("/{student_id}")
async def update_student(student_id: int):
    return {"message": f"Update student {student_id}"}


@router.delete("/{student_id}")
async def delete_student(student_id: int):
    return {"message": f"Delete student {student_id}"}

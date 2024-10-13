from fastapi import FastAPI

from routers import students

app = FastAPI()

# Including other routes
app.include_router(students.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


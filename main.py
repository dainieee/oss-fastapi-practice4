from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI()

FILE_PATH = Path("courses.json")


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


def read_courses():
    if not FILE_PATH.exists():
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except json.JSONDecodeError:
        return []


def write_courses(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/courses")
def get_courses():
    return read_courses()


@app.post("/courses")
def add_course(course: Course):
    courses = read_courses()
    courses.append(course.dict())
    write_courses(courses)
    return {
        "message": "course added successfully",
        "added_course": course.dict()
    }
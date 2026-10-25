
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI(title="Students Database CRUD API")

DATABASE = "students.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dob TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                course TEXT
            )
        """)


create_table()


class Student(BaseModel):
    name: str = Field(min_length=1)
    dob: str
    email: str
    phone: str | None = None
    course: str | None = None


# Home endpoint
@app.get("/")
def home():
    return {"message": "Students CRUD API is running"}


# CREATE: Add a student
@app.post("/students", status_code=201)
def create_student(student: Student):
    try:
        with get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO students (name, dob, email, phone, course)
                VALUES (?, ?, ?, ?, ?)
            """, (
                student.name, student.dob, student.email,
                student.phone, student.course
            ))
            student_id = cursor.lastrowid

        return {
            "message": "Student created successfully",
            "student_id": student_id
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )


# READ: List all students
@app.get("/students")
def get_students():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM students ORDER BY student_id"
        ).fetchall()

    return [dict(row) for row in rows]


# READ: Get one student
@app.get("/students/{student_id}")
def get_student(student_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return dict(row)


# UPDATE: Modify student details
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    try:
        with get_connection() as conn:
            cursor = conn.execute("""
                UPDATE students
                SET name = ?, dob = ?, email = ?, phone = ?, course = ?
                WHERE student_id = ?
            """, (
                student.name, student.dob, student.email,
                student.phone, student.course, student_id
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Student not found"
                )

        return {"message": "Student updated successfully"}

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409, detail="Email already exists"
        )


# DELETE: Remove a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Student not found"
            )

    return {"message": "Student deleted successfully"}

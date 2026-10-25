
# Students Database CRUD Application

## Project Description
This project is developed using Python, FastAPI, and SQLite.
It allows users to create, read, update, and delete student records.

## Technologies Used
- Python
- FastAPI
- SQLite
- Uvicorn
- Swagger UI

## Features
- Add a new student
- View all students
- View a student by ID
- Update student details
- Delete a student
- Prevent duplicate email addresses

## How to Run

1. Install the required packages:

   pip install -r requirements.txt

2. Start the application:

   uvicorn main:app --reload

3. Open the API documentation:

   http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /students | Create student |
| GET | /students | View all students |
| GET | /students/{student_id} | View one student |
| PUT | /students/{student_id} | Update student |
| DELETE | /students/{student_id} | Delete student |

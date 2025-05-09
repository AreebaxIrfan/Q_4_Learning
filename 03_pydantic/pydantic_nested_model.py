from pydantic import BaseModel, EmailStr

# Nested model for Student
class Student(BaseModel):
    id: int
    name: str
    email: EmailStr

# Nested model for Class
class SchoolClass(BaseModel):
    class_name: str
    students: list[Student]

# Main model for School
class School(BaseModel):
    name: str
    location: str
    classes: list[SchoolClass]

# Sample data
school_data = {
    "name": "Greenfield High",
    "location": "Lahore",
    "classes": [
        {
            "class_name": "Grade 10",
            "students": [
                {"id": 1, "name": "Ali", "email": "ali@example.com"},
                {"id": 2, "name": "Sara", "email": "sara@example.com"},
            ]
        },
        {
            "class_name": "Grade 11",
            "students": [
                {"id": 3, "name": "Zain", "email": "zain@example.com"},
            ]
        }
    ]
}

school = School.model_validate(school_data)
print(school.model_dump())
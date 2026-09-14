from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from model.course import Base, Course
from model.student import Student
from model.enrollment import Enrollment


load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Session = sessionmaker(bind=engine)

with Session() as session:

    # Step 1: Courses banao
    python_course = Course(name="Python Programming", duration=3)
    sql_course = Course(name="SQL Fundamentals", duration=2)
    ai_course = Course(name="AI & Machine Learning", duration=4)

    # Step 2: Students banao — enrollments seedha nested de sakte hain
    ahmed = Student(
        name="Ahmed Khan",
        email="ahmed@example.com",
        enrollments=[
            Enrollment(course=python_course),
            Enrollment(course=sql_course),
        ],
    )

    sara = Student(
        name="Sara Ali",
        email="sara@example.com",
        enrollments=[
            Enrollment(course=ai_course),
        ],
    )

    bilal = Student(
        name="Bilal Ahmad",
        email="bilal@example.com",
        enrollments=[
            Enrollment(course=python_course),
            Enrollment(course=ai_course),
        ],
    )

    # Step 3: Session mein add karo, phir commit karo
    session.add_all([python_course, sql_course, ai_course, ahmed, sara, bilal])
    session.commit()

    print("Data successfully insert ho gaya!")
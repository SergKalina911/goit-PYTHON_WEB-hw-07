""" Скрипт для заповнення бази даних випадковими даними за допомогою бібліотеки Faker.
Створює групи, вчителів, предмети, студентів та оцінки. """

from random import randint, choice
from faker import Faker
from connect_db import session
from models import Student, Group, Teacher, Subject, Grade

fake = Faker()

def seed_data():
    """ Функція для заповнення бази даних випадковими даними. Створює групи, вчителів, предмети,
    студентів та оцінки. """
    # Groups
    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)

    # Teachers
    teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
    session.add_all(teachers)

    # Subjects
    subjects = [Subject(name=fake.job(), teacher=choice(teachers)) for _ in range(8)]
    session.add_all(subjects)

    # Students
    students = [Student(fullname=fake.name(), group=choice(groups)) for _ in range(50)]
    session.add_all(students)

    session.commit()

    # Grades
    for student in students:
        for _ in range(randint(10, 20)):
            subject = choice(subjects)
            grade = randint(60, 100)
            date_of = fake.date_between(start_date="-1y", end_date="today")
            g = Grade(student=student, subject=subject, grade=grade, date_of=date_of)
            session.add(g)

    session.commit()

if __name__ == "__main__":
    seed_data()
    print("✅ База даних заповнена випадковими даними")

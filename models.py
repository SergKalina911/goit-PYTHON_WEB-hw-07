from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    students = relationship("Student", back_populates="group", cascade="all, delete")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student", cascade="all, delete")


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)

    subjects = relationship("Subject", back_populates="teacher", cascade="all, delete")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"))

    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject", cascade="all, delete")


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    grade = Column(Integer, nullable=False)
    date_of = Column(Date, nullable=False)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

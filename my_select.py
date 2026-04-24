from sqlalchemy import func, desc
from connect_db import session
from models import Student, Group, Teacher, Subject, Grade

# 1. 5 студентів із найбільшим середнім балом
def select_1():
    return session.query(
        Student.fullname,
        func.round(func.avg(Grade.grade), 2).label("avg_grade")
    ).select_from(Grade).join(Student).group_by(Student.id).order_by(desc("avg_grade")).limit(5).all()

# 2. Студент із найвищим середнім балом з певного предмета
def select_2(subject_id: int):
    return session.query(
        Student.fullname,
        func.round(func.avg(Grade.grade), 2).label("avg_grade")
    ).select_from(Grade).join(Student).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(desc("avg_grade")).limit(1).all()

# 3. Середній бал у групах з певного предмета
def select_3(subject_id: int):
    return session.query(
        Group.name,
        func.round(func.avg(Grade.grade), 2).label("avg_grade")
    ).select_from(Grade).join(Student).join(Group).filter(Grade.subject_id == subject_id).group_by(Group.id).all()

# 4. Середній бал на потоці
def select_4():
    return session.query(func.round(func.avg(Grade.grade), 2).label("avg_grade")).all()

# 5. Курси, які читає певний викладач
def select_5(teacher_id: int):
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()

# 6. Список студентів у певній групі
def select_6(group_id: int):
    return session.query(Student.fullname).filter(Student.group_id == group_id).all()

# 7. Оцінки студентів у групі з певного предмета
def select_7(group_id: int, subject_id: int):
    return session.query(Student.fullname, Grade.grade).join(Grade).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()

# 8. Середній бал викладача зі своїх предметів
def select_8(teacher_id: int):
    return session.query(
        Teacher.fullname,
        func.round(func.avg(Grade.grade), 2).label("avg_grade")
    ).select_from(Grade).join(Subject).join(Teacher).filter(Teacher.id == teacher_id).group_by(Teacher.id).all()

# 9. Курси, які відвідує студент
def select_9(student_id: int):
    return session.query(Subject.name).select_from(Grade).join(Subject).filter(Grade.student_id == student_id).distinct().all()

# 10. Курси, які певному студенту читає певний викладач
def select_10(student_id: int, teacher_id: int):
    return session.query(Subject.name).select_from(Grade).join(Subject).filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id).distinct().all()

# 11. Середній бал, який певний викладач ставить певному студентові
def select_11(student_id: int, teacher_id: int):
    return session.query(
        Student.fullname.label("student"),
        Teacher.fullname.label("teacher"),
        func.round(func.avg(Grade.grade), 2).label("avg_grade")
    ).select_from(Grade).join(Student).join(Subject).join(Teacher)\
     .filter(Student.id == student_id, Teacher.id == teacher_id)\
     .group_by(Student.id, Teacher.id).all()

# 12. Оцінки студентів у певній групі з певного предмета на останньому занятті
def select_12(group_id: int, subject_id: int):
    subquery = session.query(func.max(Grade.date_of)).join(Student)\
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id).scalar()

    return session.query(
        Student.fullname,
        Grade.grade,
        Grade.date_of
    ).join(Grade).filter(Student.group_id == group_id,
                         Grade.subject_id == subject_id,
                         Grade.date_of == subquery).all()

if __name__ == "__main__":
    print("Запит 1:", select_1())
    print("Запит 2:", select_2(1))
    print("Запит 3:", select_3(1))
    print("Запит 4:", select_4())
    print("Запит 5:", select_5(1))
    print("Запит 6:", select_6(1))
    print("Запит 7:", select_7(1, 1))
    print("Запит 8:", select_8(1))
    print("Запит 9:", select_9(1))
    print("Запит 10:", select_10(1, 1))
    print("Запит 11:", select_11(1, 1))
    print("Запит 12:", select_12(1, 1))
    
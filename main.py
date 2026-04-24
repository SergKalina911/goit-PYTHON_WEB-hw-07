""" CLI для керування базою даних з моделями Teacher, Group, Subject та Student.
Підтримує наступні дії: create, list, update, remove.
Приклади використання:
1. Створити вчителя:
   python main.py -a create -m Teacher -n "Іван Іванович"
2. Створити групу:
    python main.py -a create -m Group -n "Група 1"
3. Створити предмет:
    python main.py -a create -m Subject -n "Математика" --teacher_id 1
4. Створити студента:
    python main.py -a create -m Student -n "Петро Петрович" --group_id 1
5. Вивести список вчителів:
    python main.py -a list -m Teacher
6. Оновити ім'я вчителя з id=1:
    python main.py -a update -m Teacher --id 1 -n "Іван Іванович Сидоров"
7. Видалити вчителя з id=1:
    python main.py -a remove -m Teacher --id 1
"""
import argparse
from connect_db import session
from models import Teacher, Group, Subject, Student

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"], required=True)
parser.add_argument("-m", "--model", choices=["Teacher", "Group", "Subject", "Student"], required=True)
parser.add_argument("-n", "--name")
parser.add_argument("--id", type=int)
parser.add_argument("--teacher_id", type=int)
parser.add_argument("--group_id", type=int)
args = parser.parse_args()

# ---------- CREATE ----------
def create_teacher(name):
    """ Створює нового вчителя з заданим ім'ям."""
    teacher = Teacher(fullname=name)
    session.add(teacher)
    session.commit()
    print(f"✅ Створено Teacher: {name}")

def create_group(name):
    """ Створює нову групу з заданим ім'ям."""
    group = Group(name=name)
    session.add(group)
    session.commit()
    print(f"✅ Створено Group: {name}")

def create_subject(name, teacher_id):
    """ Створює новий предмет з заданим ім'ям та id вчителя."""
    subject = Subject(name=name, teacher_id=teacher_id)
    session.add(subject)
    session.commit()
    print(f"✅ Створено Subject: {name} (teacher_id={teacher_id})")

def create_student(name, group_id):
    """ Створює нового студента з заданим ім'ям та id групи."""
    student = Student(fullname=name, group_id=group_id)
    session.add(student)
    session.commit()
    print(f"✅ Створено Student: {name} (group_id={group_id})")

# ---------- LIST ----------
def list_all(model):
    """ Виводить всі записи для заданої моделі."""
    items = session.query(model).all()
    for item in items:
        print(item)

# ---------- UPDATE ----------
def update_teacher(id, name):
    """ Оновлює ім'я вчителя з заданим id."""
    teacher = session.query(Teacher).get(id)
    if teacher:
        teacher.fullname = name
        session.commit()
        print(f"✏️ Оновлено Teacher {id}: {name}")

def update_group(id, name):
    """ Оновлює ім'я групи з заданим id."""
    group = session.query(Group).get(id)
    if group:
        group.name = name
        session.commit()
        print(f"✏️ Оновлено Group {id}: {name}")

def update_subject(id, name):
    """ Оновлює ім'я предмета з заданим id."""
    subject = session.query(Subject).get(id)
    if subject:
        subject.name = name
        session.commit()
        print(f"✏️ Оновлено Subject {id}: {name}")

def update_student(id, name):
    """ Оновлює ім'я студента з заданим id."""
    student = session.query(Student).get(id)
    if student:
        student.fullname = name
        session.commit()
        print(f"✏️ Оновлено Student {id}: {name}")

# ---------- REMOVE ----------
def remove(model, id):
    """ Видаляє запис заданої моделі з заданим id."""
    item = session.query(model).get(id)
    if item:
        session.delete(item)
        session.commit()
        print(f"❌ Видалено {model.__name__} {id}")
    else:
        print(f"⚠️ {model.__name__} з id={id} не знайдено")

# ---------- MAIN ----------
if args.action == "create":
    if args.model == "Teacher":
        create_teacher(args.name)
    elif args.model == "Group":
        create_group(args.name)
    elif args.model == "Subject":
        create_subject(args.name, args.teacher_id)
    elif args.model == "Student":
        create_student(args.name, args.group_id)

elif args.action == "list":
    if args.model == "Teacher":
        list_all(Teacher)
    elif args.model == "Group":
        list_all(Group)
    elif args.model == "Subject":
        list_all(Subject)
    elif args.model == "Student":
        list_all(Student)

elif args.action == "update":
    if args.model == "Teacher":
        update_teacher(args.id, args.name)
    elif args.model == "Group":
        update_group(args.id, args.name)
    elif args.model == "Subject":
        update_subject(args.id, args.name)
    elif args.model == "Student":
        update_student(args.id, args.name)

elif args.action == "remove":
    if args.model == "Teacher":
        remove(Teacher, args.id)
    elif args.model == "Group":
        remove(Group, args.id)
    elif args.model == "Subject":
        remove(Subject, args.id)
    elif args.model == "Student":
        remove(Student, args.id)

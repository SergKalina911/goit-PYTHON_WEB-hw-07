# goit-PYTHON_WEB-hw-07

Домашнє завдання №7 курсу Python WEB в GO IT

---

## 📌 Опис

Навчальний проєкт для роботи з PostgreSQL, SQLAlchemy ORM, Alembic та Docker.  
Мета — створити базу даних для студентів, викладачів, груп і предметів, засіяти її випадковими
даними та реалізувати ORM запити й CRUD через CLI.

---

## 📌 Оригінал завдання

### Домашнє завдання #7

#### Вступна

У цьому домашньому завданні ми продовжимо працювати з домашнім завданням із попереднього модуля.

В цій домашній роботі використаємо базу даних postgres. У командному рядку запустіть Docker контейнер:

docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

Замість some-postgres виберіть свою назву контейнера, а замість mysecretpassword придумайте свій пароль для підключення до бази даних

👉 CAUTION
За домовленістю з ментором та технічною неможливістю використовувати postgres, можна замінити
її на SQLite

#### Кроки виконання домашнього завдання

##### Перший крок

Реалізуйте свої моделі SQLAlchemy, для таблиць:

• Таблиця студентів;
• Таблиця груп;
• Таблиця викладачів;
• Таблиця предметів із вказівкою викладача, який читає предмет;
• Таблиця де кожен студент має оцінки з предметів із зазначенням коли оцінку отримано;

##### Другий крок

Використовуйте alembic для створення міграцій у базі даних.

##### Третій крок

Напишіть скрипт seed.py та заповніть отриману базу даних випадковими даними (~30-50 студентів, 3 групи, 5-8 предметів, 3-5 викладачів, до 20 оцінок у кожного студента з усіх предметів). Використовуйте пакет Faker для наповнення. При заповненні використовуємо механізм сесій SQLAlchemy.

##### Четвертий крок

Зробити такі вибірки з отриманої бази даних:

1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
2. Знайти студента із найвищим середнім балом з певного предмета.
3. Знайти середній бал у групах з певного предмета.
4. Знайти середній бал на потоці (по всій таблиці оцінок).
5. Знайти які курси читає певний викладач.
6. Знайти список студентів у певній групі.
7. Знайти оцінки студентів у окремій групі з певного предмета.
8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
9. Знайти список курсів, які відвідує певний студент.
10. Список курсів, які певному студенту читає певний викладач.

Для запитів оформити окремий файл my_select.py, де будуть 10 функцій від select_1 до select_10. Виконання функцій повинно повертати результат аналогічний попередньої домашньої роботи. При запитах використовуємо механізм сесій SQLAlchemy.

#### Підказки та рекомендації

Це завдання перевірить вашу здатність користуватися документацією SQLAlchemy. Але основні підказки та напрямки рішення ми вам дамо одразу. Нехай у нас є наступний запит.

Знайти 5 студентів з найбільшим середнім балом з усіх предметів.

    SELECT s.fullname, round(avg(g.grade), 2) AS avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 5;

Спробуймо його перевести в запит ORM SQLAlchemy. Нехай у нас є сесія у змінній session. Є описані моделі Student та Grade для відповідних таблиць.

Вважаємо, що база даних вже заповнена даними. Функції агрегації SQLAlchemy зберігає в об'єкті func. Його треба спеціально імпортувати from sqlalchemy import func і тоді ми зможемо використати методи func.round та func.avg. Отже перший рядок SQL запиту має виглядати так session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')). Тут ми використали ще label('avg_grade') так ORM виконує найменування поля, із середнім балом, за допомогою оператора AS.

Далі FROM grades g замінюється методом select_from(Grade). Заміна оператора JOIN - тут все просто це функція join(Student), все інше на себе бере ORM. Групування по полю виконуємо функцією group_by(Student.id).

За сортування відповідає функція order_by, яка, за замовчуванням, сортує як ASC, а нам явно треба режим зростання DESC та ще й по полю avg_grade, яке ми самі створили у запиті. Імпортуємо from sqlalchemy import func, desc та остаточний вигляд — order_by(desc('avg_grade')). Ліміт у п'ять значень це функція з такою самою назвою limit(5). Ось і все, наш запит готовий.

Остаточний варіант запиту для ORM SQLAlchemy.

session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
 .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

Можливе виведення:

[('Mary Smith', Decimal('8.33')), ('Kimberly Howard', Decimal('8.17')), ('Gregory Graves', Decimal('7.92')), ('Mrs. Diamond Carter', Decimal('7.53')), ('Emma Hernandez', Decimal('7.31'))]

Інші запити ви повинні побудувати аналогічно викладеному вище прикладу. І остання підказка, якщо ви вирішите зробити вкладені запити, тоді використовуйте scalar-selects

#### Додаткове завдання

##### Перша частина

Для додаткового завдання зробіть такі запити підвищеної складності:

1. Середній бал, який певний викладач ставить певному студентові.
2. Оцінки студентів у певній групі з певного предмета на останньому занятті.

##### Друга частина

Замість скрипту seed.py подумайте та реалізуйте повноцінну CLI програму для CRUD операцій із базою даних. Використовуйте для цього модуль argparse .

Використовуйте команду --action або скорочений варіант -a для CRUD операцій. Та команду --model (-m) для вказівки над якою моделлю проводитися операція.

Приклад:

• --action create -m Teacher --name 'Boris Jonson' створення вчителя
• --action list -m Teacher показати всіх вчителів
• --action update -m Teacher --id 3 --name 'Andry Bezos' оновити дані вчителя з id=3
• --action remove -m Teacher --id 3 видалити вчителя з id=3

Реалізуйте ці операції для кожної моделі.

👉INFO

    Приклади виконання команд у терміналі.

        Створити вчителя

            py main.py -a create -m Teacher -n 'Boris Jonson'

        Створити групу

            py main.py -a create -m Group -n 'AD-101'

---

## 📂 Структура репозиторію

```text
hw07/
├── alembic/                     # Папка для міграцій Alembic
│   ├── versions/                # Автоматично згенеровані файли міграцій
│   ├── env.py                   # Налаштування Alembic
│   └── alembic.ini              # Конфігурація Alembic
├── connect_db.py                # Підключення до БД (PostgreSQL)
├── models.py                    # ORM-моделі: Student, Group, Teacher, Subject, Grade
├── seed.py                      # Faker-дані для заповнення БД
├── my_select.py                 # 12 функцій ORM-запитів
├── main.py                      # CLI-програма для CRUD-операцій
├── README.md                    # Документація проєкту
├── docker-compose.yml           # Конфігурація Docker з таймзоною Europe/Kyiv
├── pyproject.toml               # Основний файл Poetry із залежностями
└── poetry.lock                  # Зафіксовані версії бібліотек
```

## ⚙️ Встановлення, перевірка та запуск

### 1. Клонування репозиторію

```bash
git clone <https://github.com/SergKalina911/goit-PYTHON_WEB-hw-07.git>
cd goit-python-web-hw-07
```

### 2. Віртуальне середовище (Poetry)

```bash
poetry install
poetry shell
```

### 3. Docker Compose

#### Файл docker-compose.yml:

    version: "3.9"
    services:
    postgres:
    image: postgres:16
    container_name: school-postgres
    restart: always
    environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: mysecretpassword
    POSTGRES_DB: school
    ports: - "5432:5432"
    volumes: - postgres_data:/var/lib/postgresql/data
    command: ["postgres", "-c", "timezone=Europe/Kyiv"]

    volumes:
    postgres_data:

#### Запуск:

```bash
docker compose up -d
```

#### Перевірка таймзони:

```bash
docker exec -it school-postgres psql --username=postgres -c "SHOW TIMEZONE;"
```

👉 має показати Europe/Kyiv.

### 4. 📊 Структура бази даних

```text
    • Teachers (id, fullname)
    • Groups (id, name)
    • Students (id, fullname, group_id)
    • Subjects (id, name, teacher_id)
    • Grades (id, student_id, subject_id, grade, date_received)
```

### 5. 📥 Міграції Alembic

1. Створення ревізії

```bash
alembic revision --autogenerate -m "Init"
```

2. Застосування міграцій

```bash
alembic upgrade head
```

3. Перевірка таблиць

```bash
docker exec -it school-postgres psql --username=postgres -d school -c "\dt"
```

### 6. 📥 Засівання даних

```bash
python seed.py
```

👉 створює випадкові дані за допомогою Faker.

### 7. 📈 ORM запити

Файл my_select.py містить 12 запитів:

1.  Топ 5 студентів за середнім балом.
2.  Студент з найвищим середнім балом.
3.  Середній бал по групах.
4.  Середній бал по всіх студентах.
    5 - 12. Аналітичні вибірки (предмети викладачів, оцінки студентів, останні дати тощо).

Запуск:

```bash
python my_select.py
```

### 8. 🔧 CRUD через CLI

Файл main.py підтримує всі дії для моделей Teacher, Group, Subject, Student.

#### ➕ Створення

```bash
python main.py -a create -m Teacher -n "John Smith"
python main.py -a create -m Group -n "Group 4"
python main.py -a create -m Subject -n "Mathematics" --teacher_id 1
python main.py -a create -m Student -n "Alice Johnson" --group_id 2
```

#### 📋 Перегляд

```bash
python main.py -a list -m Teacher
python main.py -a list -m Group
python main.py -a list -m Subject
python main.py -a list -m Student
```

#### ✏️ Оновлення

```bash
python main.py -a update -m Teacher --id 1 -n "John A. Smith"
python main.py -a update -m Group --id 2 -n "Group 2A"
```

#### ❌ Видалення

```bash
python main.py -a remove -m Subject --id 1
python main.py -a remove -m Student --id 5
```

### 9. 📌 Повний сценарій CRUD

#### Створення викладача

```bash
python main.py -a create -m Teacher -n "John Smith"
```

#### Створення групи

```bash
python main.py -a create -m Group -n "Group 4"
```

#### Створення предмета

```bash
python main.py -a create -m Subject -n "Mathematics" --teacher_id 1
```

#### Створення студента

```bash
python main.py -a create -m Student -n "Alice Johnson" --group_id 2
```

#### Перегляд викладачів

```bash
python main.py -a list -m Teacher
```

#### Оновлення викладача

```bash
python main.py -a update -m Teacher --id 1 -n "John A. Smith"
```

#### Видалення предмета

```bash
python main.py -a remove -m Subject --id 1
```

# ✅ Підсумок

• Docker Compose налаштований із таймзоною Europe/Kyiv.
• Alembic використовується для міграцій, усі ревізії зберігаються в alembic/versions/
• База даних створена й засіяна Faker-ом.
• ORM запити працюють (my_select.py).
• CRUD через CLI реалізовано для всіх моделей (main.py).
• Poetry використовується для керування залежностями (pyproject.toml, poetry.lock).

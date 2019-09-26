from app import db, user_manager
from app.models import User, Role, Student
from flask_user import ConfigError
import csv
import warnings


def add_user(username, roles=[]):
    roles = list(roles)
    print(f'Adding user={username}; roles={roles}')
    if not User.query.filter(User.username == username).first():
        user = User(
            username=username,
            password=user_manager.hash_password(input(f"Insert password for {username}: ")),
        )
        for role in roles:
            user.roles.append(Role(name=role))

        db.session.add(user)
        db.session.commit()
        print(f"User {username} successfully added!")
    else:
        raise ConfigError(f"Username {username} already exists!")


def load_students(students_file, academic_year):
    with open(students_file, 'r') as f:
        print(f"Loading students from file {students_file}...")
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if Student.query.filter(db.text(f"jmbag = '{row['JMBAG']}'")).count() > 0:
                warnings.warn(f"Student {row['JMBAG']} already exists - skipping!")
                continue
            student = Student(
                jmbag=row['JMBAG'],
                first_name=row['Ime'],
                last_name=row['Prezime']
            )
            db.session.add(student)
        db.session.commit()
        print("Done!")

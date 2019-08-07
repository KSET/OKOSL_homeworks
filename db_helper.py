from app import db, user_manager
from app.models import User, Role
from flask_user import ConfigError


def add_user(username, roles=[]):
    roles = list(roles)
    print(f'user={username}; roles={roles}')
    print(type(roles))
    if not User.query.filter(User.username == username).first():
        user = User(
            username=username,
            password=user_manager.hash_password(input(f"Insert password for {username}: ")),
        )
        for role in roles:
            user.roles.append(Role(name=role))

        db.session.add(user)
        db.session.commit()
    else:
        raise ConfigError(f"Username {username} already exists!")

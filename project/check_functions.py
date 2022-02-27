from project.models import User


def check_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return True
    return False


def check_email(email):
    email = User.query.filter_by(email=email).first()
    if email:
        return True
    return False

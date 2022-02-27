from functools import wraps
from flask import request, jsonify
import jwt
from project.models import User
from . import app

from itsdangerous import URLSafeTimedSerializer


def login_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.form:
            token = request.form["token"]

        if not token:
            return jsonify({'message': 'Token is missing!'})

        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = User.query.filter_by(id=data['id']).first()

        return f(current_user, *args, **kwargs)

    return decorated


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'])
    except:
        return False
    return email

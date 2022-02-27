import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__, template_folder='template')

##
# start config
##

app.config['SECRET_KEY'] = 'cvaFwrlLifCSCrqww9EnVgtDfH9omagr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'

app.config["JWT_SECRET_KEY"] = 'NKzaz6EZ1sckfnMEvQzJxp2WANn0aHRs52olHLNW_JU'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['MAIL_USERNAME'] = "cards.send.confirmation@gmail.com"
app.config['MAIL_PASSWORD'] = "focfaw-paCbo5-woqxid"

app.config['MAIL_DEFAULT_SENDER'] = 'from@example.com'

##
# end config
##

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
jwt = JWTManager(app)

db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

from project import routes
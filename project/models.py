from array import array
from dataclasses import dataclass

from cffi.backend_ctypes import long

from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@dataclass
class AdditionalInfo(db.Model):
    __tablename__ = "additionalInfo"
    id: int = db.Column(db.Integer, primary_key=True)
    city: str = db.Column(db.String, nullable=False)
    country: str = db.Column(db.String, nullable=False)
    description: str = db.Column(db.String, nullable=False)
    typeOfWork: str = db.Column(db.String, nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"AdditionalInfo('{self.description}', '{self.country}')"


@dataclass
class Profession(db.Model):
    __tablename__ = "profession"
    id: int = db.Column(db.Integer, primary_key=True)
    description: str = db.Column(db.String, nullable=False)
    specialization: str = db.Column(db.String, nullable=False)
    tags: list = db.Column(db.PickleType, nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Profession('{self.description}', '{self.specialization}')"


@dataclass
class Card(db.Model):
    __tablename__ = "card"
    id: str = db.Column(db.String, primary_key=True)
    title: str = db.Column(db.String(), nullable=False)
    description: str = db.Column(db.String(), nullable=False)
    date: str = db.Column(db.String(), nullable=False)
    createTime: long = db.Column(db.Integer, nullable=False)
    cost: int = db.Column(db.Integer, nullable=False)
    active: bool = db.Column(db.Boolean, nullable=False)
    agreement: bool = db.Column(db.Boolean, nullable=False)
    user_id: str = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Card('{self.title}', '{self.description}', '{self.date}', '{self.createTime}', '{self.cost}', '{self.active}', '{self.agreement}')"


@dataclass
class Token(db.Model):
    __tablename__ = "token"
    id: int = db.Column(db.Integer, primary_key=True)
    token: str = db.Column(db.String)
    user_id: str = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)


@dataclass
class Image(db.Model):
    __tablename__ = "image"
    id: int = db.Column(db.Integer, primary_key=True)
    img: str = db.Column(db.Text, unique=True, nullable=False)
    name: str = db.Column(db.Text, nullable=False)
    mimeType: str = db.Column(db.Text, nullable=False)
    user_id: str = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)


@dataclass
class User(db.Model):
    __tablename__ = "user"
    id: str = db.Column(db.String, primary_key=True)
    username: str = db.Column(db.String())
    email: str = db.Column(db.String(), unique=True)
    password: str = db.Column(db.String())
    rating: float = db.Column(db.Float)
    isExecutor: bool = db.Column(db.Boolean)
    confirmed: bool = db.Column(db.Boolean, default=False)
    tokens: list[Token] = db.relationship("Token", backref="user", lazy=True)
    additionalInfo: AdditionalInfo = db.relationship("AdditionalInfo", backref="user", uselist=False)
    profession: Profession = db.relationship("Profession", backref="user", uselist=False)
    profileImg: Image = db.relationship("Image", backref="user", uselist=False)
    cards: list[Card] = db.relationship('Card', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.tokens}', {self.cards})"

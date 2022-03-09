from array import array
from dataclasses import dataclass
from sys import maxsize
from typing import Any

from cffi.backend_ctypes import long

from . import db, login_manager
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields


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
class User(db.Model):
    __tablename__ = "user"
    id: str = db.Column(db.String, primary_key=True)
    username: str = db.Column(db.String(), unique=True, nullable=False)
    email: str = db.Column(db.String(), unique=True, nullable=False)
    password: str = db.Column(db.String(), nullable=False)
    rating: float = db.Column(db.Float, nullable=False)
    isExecutor: bool = db.Column(db.Boolean, nullable=False)
    confirmed: bool = db.Column(db.Boolean, nullable=False, default=False)
    additionalInfo: AdditionalInfo = db.relationship("AdditionalInfo", backref="user", uselist=False)
    profession: Profession = db.relationship("Profession", backref="user", uselist=False)
    cards: list[Card] = db.relationship('Card', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}, {self.username}', '{self.email}', '{self.password}')"



from .. import db, flask_bcrypt, ma
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
import jwt
from typing import Union


class Game(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "plays"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    gamenumbers = db.Column(db.String(100), unique=True)
    creation_date =  db.Column(db.DateTime, nullable=False)


    def __init__(self, public_id, gamenumbers, creation_date):
        self.public_id = public_id
        self.gamenumbers = gamenumbers
        self.creation_date = creation_date

  
    def __repr__(self):
        return f'Game {self.username}'

class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id','gamenumbers')

game_share_schema = GameSchema()
games_share_schema = GameSchema(many=True)
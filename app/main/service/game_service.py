import datetime
import sys
import uuid
from random import randint
from typing import Dict, Tuple

from app.main import db
from app.main.model.game import Game, game_share_schema, games_share_schema

NUMERO_DEZENAS = 6

def save_new_game(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:

        new_game = Game(
            public_id=data['public_id'],
            gamenumbers=data['gamenumbers'],
            creation_date=datetime.datetime.utcnow()
        )
        save_changes(new_game)
        GameID = game_share_schema.dump(
            Game.query.filter_by(username=new_game.public_id).first()
        )
       
        response_object = {
            'status': 'success',
            'message': 'Game created successfully!',
        }
        return response_object, 201


def get_all_game_by_user(public_id):
    return Game.query.filter_by(public_id=public_id).first()


def get_by_game_by_user(public_id):
    return Game.query.filter_by(public_id=public_id).first()

def save_changes(data: Game) -> None:
    db.session.add(data)
    db.session.commit()





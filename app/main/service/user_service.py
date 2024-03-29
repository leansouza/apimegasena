import datetime
import uuid
from typing import Dict, Tuple

from app.main import db
from app.main.model.user import User, user_share_schema, users_share_schema


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        userID = user_share_schema.dump(
            User.query.filter_by(username=new_user.username).first()
        )
        return generate_token(userID['id'])
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    
    return User.query.filter_by(public_id=public_id).first()


def get_user_delete(public_id):
    delete_user = User.query.filter_by(public_id=public_id).delete()
    
   
    if delete_user:
        response_object = {
            'status': 'success',
            'message': 'User removed successfully!',
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'could not remove user',
        }
        return response_object, 409

    
    


def generate_token(user: User) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data: User) -> None:
    db.session.add(data)
    db.session.commit()


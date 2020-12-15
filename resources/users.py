import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel
        
class UserRegister(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username',
            type=str,
            required=True,
            help="Please provide a username"
        )
        parser.add_argument('password',
            type=str,
            required=True,
            help="Please provide a password"
        )
        data=parser.parse_args()

        if UserModel.find_user_by_username(data['username']):
            return{'message':'the user is already present in the database'},400

        user=UserModel(**data)
        user.save_to_db()
        return {'message':'user has been added'},201
            

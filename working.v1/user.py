from db import db
from flask_restful import Resource,reqparse
from sqlalchemy import create_engine
from flask_jwt import jwt_required
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from auth import Auth
Base=automap_base()
class User(db.Model):
    __tablename__ = 'user'
    __table__ = db.Table('user', Base.metadata,
                    autoload=True, autoload_with=db.engine)

    def __init__(self,User_Name,First_Name,Last_Name,User_Email,phone_no,password):
        self.User_Name=User_Name
        self.First_Name=First_Name
        self.Last_Name=Last_Name
        self.User_Email=User_Email
        self.phone_no=phone_no
        self.password=password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'User_id':self.User_id,'User_Name': self.User_Name, 'First_Name': self.First_Name,'Last_Name': self.Last_Name,'User_Email': self.User_Email,'phone_no':self.phone_no,'Role':self.Role_id}

    @classmethod
    def find_by_name(cls, User_Name):
        print(User_Name)
        val= cls.query.filter_by(User_Name=User_Name).first()
        print(val)
        return val


class UserSignup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('User_Name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('First_Name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('Last_Name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('User_Email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('phone_no',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    def post(self): 
        data = UserSignup.parser.parse_args()
        user = User(data['User_Name'],data['First_Name'],data['Last_Name'],data['User_Email'],data['phone_no'],None)
        auth = Auth(None,data['User_Name'],data['password'])
        if User.find_by_name(data['User_Name']):
            return {'message': "A store with name '{}' already exists.".format(data['User_Name'])}, 400
        
        user.save_to_db()
        auth.save_to_db()
        return {"message": "User created successfully."}, 201

class UserAccount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('User_Name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('First_Name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('Last_Name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('User_Email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('phone_no',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    @jwt_required()
    def get(self,User_Name):
        user=User.find_by_name(User_Name)
        if user:
            return user.json()
        return {'message': 'Item not found'}, 404

    def put(self, User_Name):
        data = UserAccount.parser.parse_args()

        user = User.find_by_name(User_Name)

        if user:
            user.User_Name=data['User_Name']
            user.First_Name=data['First_Name']
            user.Last_Name=data['Last_Name']
            user.User_Email=data['User_Email']
            user.phone_no=data['phone_no']
        else:
            user = User(User_Name, **data)

        user.save_to_db()

        return user.json()

    


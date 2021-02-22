from db import db
from blacklist import BLACKLIST
from flask import Flask,jsonify,Response,make_response
from flask_restful import Resource,reqparse
from sqlalchemy import create_engine
from flask_jwt_extended import jwt_required,create_access_token,create_refresh_token,get_jwt_identity,get_jti
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from auth import Auth
from passlib.context import CryptContext
import smtplib
Base=automap_base()

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def prepare_response(res_object, status_code):
    response = jsonify(res_object)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    return make_response(response, status_code)

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

    def encrypt_password(password):
        return pwd_context.encrypt(password)

    def check_encrypted_password(password, hashed):
        return pwd_context.verify(password, hashed)

    @classmethod
    def find_by_name(cls, User_Name):
        print(User_Name)
        val= cls.query.filter_by(User_Name=User_Name).first()
        print(val)
        return val

    @classmethod
    def find_by_email(cls, User_Email):
        print(User_Name)
        val= cls.query.filter_by(User_Email=User_Email).first()
        print(val)
        return val

    @classmethod
    def find_by_id(cls, User_id):
        print(User_id)
        val= cls.query.filter_by(id=User_id).first()
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
        user.save_to_db()
        userid=User.find_by_name(data['User_Name'])
        password=User.encrypt_password(data['password'])
        auth = Auth(userid.User_id,data['User_Name'],password)
        """ if User.find_by_name(data['User_Name']):
            return {'message': "A store with name '{}' already exists.".format(data['User_Name'])}, 400 """
        
        
        auth.save_to_db()
        cur_user=User.find_by_name(data['User_Name'])
        return prepare_response(cur_user.json(),201)

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('User_Name',
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
        data = UserLogin.parser.parse_args()
        user=User.find_by_name(data['User_Name'])
        auth=Auth.find_by_name(data['User_Name'])
        if user and User.check_encrypted_password(data['password'],auth.password):
            access_token = create_access_token(identity=auth.id,fresh=True)
            refresh_token = create_refresh_token(auth.id)
            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            },200
        return {'message':'Invalid credentials'},401

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        return {'access_token': new_token},200

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti=get_jti()
        BLACKLIST.add(jti)
        return {'message':'User successfully logged out'},200

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

class GetMail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('User_Email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    def post(self):
        data = GetMail.parser.parse_args()
        gmail_user = 'JediSchoolTeam3@gmail.com'
        gmail_password = 'PractoTeam3@JediSchool'

        sent_from = gmail_user
        to = [data['User_Email']]
        subject = 'Welcome to Task Tracker'
        email_text = "You are invited to Join Team1\n\n Click on the Link below to Signup and Join the team.\n https://practotasktracker.netlify.app/\n\n Regards,\nJediSchoolTeam3"
        message = 'Subject: {}\n\n{}'.format(subject, email_text)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()
        return {'message':'Mail sent!'}

    

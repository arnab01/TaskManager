from itsdangerous import URLSafeTimedSerializer
from db import db
from tasks import mail
from flask import Flask,jsonify,Response,make_response
from flask_restful import Resource,reqparse
from sqlalchemy import create_engine
from flask_jwt import jwt_required
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from auth import Auth
from user import User,prepare_response
from passlib.context import CryptContext
import smtplib
Base=automap_base()
url=''
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

class Invite(db.Model):
    __tablename__ = 'invite'
    __table__ = db.Table('invite', Base.metadata,
                    autoload=True, autoload_with=db.engine)
    
    def __init__(self,_id,email,token,confirmed):
        self.id=_id
        self.email=email
        self.token=token
        self.confirmed=confirmed
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def encrypt_token(email):
        return pwd_context.encrypt(email)

    def check_encrypted_token(email, hashed):
        return pwd_context.verify(email, hashed)

    @classmethod
    def find_by_name(cls, email):
        val= cls.query.filter_by(email=email).first()
        print(val)
        return val


class Mail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    def post(self):
        data = Mail.parser.parse_args()
        token=Invite.encrypt_token(data['email'])
        val= Invite(None,data['email'],token,0)
        val.save_to_db()
        url="https://practotasktracker.netlify.app/signup/"
        url=url+str(token)
        """ gmail_user = 'JediSchoolTeam3@gmail.com'
        gmail_password = 'PractoTeam3@JediSchool'

        sent_from = gmail_user
        to = [data['email']]
        url="https://practotasktracker.netlify.app/signup/"
        url=url+str(token)
        subject = 'Welcome to Task Tracker'
        email_text = "You are invited to Join Team1\n\n Click on the Link below to Signup and Join the team.\n "+url+"\n\n Regards,\nJediSchoolTeam3"
        message = 'Subject: {}\n\n{}'.format(subject, email_text)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close() """
        mail.delay(data['email'])
        return {'message':'Mail sent!'}

class CheckEmail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('token',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    
    def post(self,token):
    data = CheckEmail.parser.parse_args()
    result = db.session.query(Invite).filter(Invite.token.like(data['token']))
    for row in result:
        val=row.token
        email=row.email
    if User.check_encrypted_token(token,val):
        user=User.find_by_email(email)
        if user:
            return prepare_response({'Message':'You have already registered.Please Login'},200)
        else:
            invite=Invite.find_by_name(email)
            invite.confirmed=1
            invite.save_to_db()
            return prepare_response({'User_Email':email},200)
    else:
        return prepare_response({'message':'Invalid user'},401)

class InviteSignup(Resource):
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
    parser.add_argument('token',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    
    def post(self): 
        data = UserSignup.parser.parse_args()
        result = db.session.query(Invite).filter(Invite.token.like(data['token']))
        for row in result:
            val=row.token
            email=row.email
        if User.check_encrypted_token(token,val):
            user=User.find_by_email(email)
            if user:
                return {'Message':'You have already registered.Please Login'}
            else:
                invite=Invite.find_by_name(email)
                invite.confirmed=1
                invite.save_to_db()
                return {'User_Email':email}
        else:
            return {'message':'Invalid user'}
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

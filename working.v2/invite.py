from itsdangerous import URLSafeTimedSerializer
from db import db
from flask import Flask,jsonify,Response,make_response
from flask_restful import Resource,reqparse
from sqlalchemy import create_engine
from flask_jwt import jwt_required
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
        gmail_user = 'JediSchoolTeam3@gmail.com'
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
        server.close()
        return {'message':'Mail sent!'}

    def get(self,token):
        result = db.session.query(Task).filter(Invite.token.like(token))
        if User.check_encrypted_password(password,user.password)
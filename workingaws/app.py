#!/usr/bin/env/ python3

from flask import Flask,redirect, url_for, request
from flask_restful import Api,Resource
from flask_jwt import JWT
from security import authenticate, identity
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from auth import UserRegister
from user import UserSignup,UserAccount

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://admin:12345678@mysql-dbms.cjxt3oa51lw1.ap-south-1.rds.amazonaws.com/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'vishal'
api = Api(app)

from sqlalchemy.orm import relationship, backref

jwt = JWT(app, authenticate, identity) 

class trail(Resource):
    def get(self):
        return 'App Working'

api.add_resource(trail,'/')
api.add_resource(UserRegister, '/register')   
api.add_resource(UserSignup, '/signup')
api.add_resource(UserAccount, '/account/<string:User_Name>')  
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0',port='8000',debug=True)

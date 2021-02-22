from flask import Flask,redirect, url_for, request
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from user import UserRegister

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:vishal@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'vishal'
api = Api(app)

from sqlalchemy.orm import relationship, backref

jwt = JWT(app, authenticate, identity) 




""" @app.route('/', methods=['get'])
def index():
    result = db.session.query(user).all()
    for r in result:
       print(r.User_Name)
    return 'done!' """

""" @app.route('/signup', methods=['get','post'])
def signup():
    if request.method=='post':
        data.save_to_db()
        return "done!"
    if request.method=='get':
        user= """

""" @app.route('/createtask',methods=['post'])
def create():
    pass """

api.add_resource(UserRegister, '/register')   

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
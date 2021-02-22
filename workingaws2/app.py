#!/usr/bin/env/ python3
from flask import Flask,redirect, url_for, request
from flask_restful import Api
from flask_jwt_extended import JWTManager,get_jti
import datetime
from blacklist import BLACKLIST
#from security import authenticate, identity
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from auth import UserRegister
from user import UserSignup,UserAccount,GetMail,UserLogin,TokenRefresh,UserLogout
from task import CreateTask,GetTask,PutStatus,GetUserTask,SortPriority,SortPD,DeleteTask,SortPDbyUser,SortPrioritybyUser
from flask_cors import CORS
from invite import Mail
from team import GetTeams,GetUserNames,InviteeSignup
app=Flask(__name__)
JWT_EXPIRES = datetime.timedelta(seconds=120*60)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://admin:12345678@mysql-dbms.cjxt3oa51lw1.ap-south-1.rds.amazonaws.com/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']
app.secret_key = 'vishal'
api = Api(app)
CORS(app)
jwt = JWTManager(app)


from sqlalchemy.orm import relationship, backref


api.add_resource(InviteeSignup, '/InviteeSignup/<string:Team_Name>')
api.add_resource(SortPD, '/sortpd/<string:Team_Name>')
api.add_resource(SortPDbyUser, '/sortpduser/<string:User_Name>')
api.add_resource(SortPriority, '/sortp/<string:Team_Name>')
api.add_resource(SortPrioritybyUser, '/sortpuser/<string:User_Name>')
api.add_resource(GetTeams, '/getteams')
api.add_resource(GetUserTask, '/usertask/<string:User_Name>')
api.add_resource(GetUserNames, '/users/<string:Team_Name>')    
api.add_resource(GetTask, '/task/<string:Team_Name>') 
api.add_resource(PutStatus, '/tasks/<string:Task_id>') 
api.add_resource(DeleteTask,'/deletetask/<string:Task_id>')
api.add_resource(CreateTask, '/createtask') 
api.add_resource(UserRegister, '/register')   
api.add_resource(UserSignup, '/signup')
api.add_resource(GetMail, '/mail')
api.add_resource(Mail, '/email')
api.add_resource(Mail, '/email/<string:token>')
api.add_resource(UserAccount, '/account/<string:User_Name>')
api.add_resource(UserLogin,'/login')  
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(UserLogout,'/logout')
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
#!/usr/bin/env/ python3
from db import db
from flask import jsonify
from flask_restful import Resource,reqparse
from sqlalchemy import create_engine
from flask_jwt import jwt_required
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from user import User,prepare_response
from auth import Auth

Base=automap_base()
class Team(db.Model):
    __tablename__ = 'Teams'
    __table__ = db.Table('Teams', Base.metadata,
                    autoload=True, autoload_with=db.engine)

    def __init__(self,Team_id,Team_Name):
        self.Team_Name=Team_Name
        self.Team_id=Team_id

class Team_User(db.Model):
    __tablename__ = 'user_team_mapping'
    __table__ = db.Table('user_team_mapping', Base.metadata,
                    autoload=True, autoload_with=db.engine)

    def __init__(self,Team_id,User_id):
        self.User_id=User_id
        self.Team_id=Team_id       

class GetTeams(Resource):
    @jwt_required()
    def get(self):
        result=Team.query.all()
        teams=[]
        for row in result:
            teams.append({'Team_id':row.Team_id,'Team_Name': row.Team_Name})
        if teams:
            return prepare_response(teams,200)
        return prepare_response({'message': 'No teams not found'}, 404)


class GetUserNames(Resource):
    @jwt_required()
    def get(self,Team_Name):
        users=[]
        result= db.session.query(User.User_Name,User,Team,Team_User).filter(User.User_id==Team_User.User_id).filter(Team.Team_id==Team_User.Team_id).filter(Team.Team_Name.like(Team_Name))        
        for row in result:
            users.append({'User_Name':row.User_Name})
        if users:
            return prepare_response(users,200)
        return prepare_response({'message': 'User not found'}, 404)

class InviteeSignup(Resource):
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
    def post(self,Team_Name): 
        data = InviteeSignup.parser.parse_args()
        user = User(data['User_Name'],data['First_Name'],data['Last_Name'],data['User_Email'],data['phone_no'],None)
        password=User.encrypt_password(data['password'])
        auth = Auth(None,data['User_Name'],password)
        if User.find_by_name(data['User_Name']):
            return prepare_response({'message': "A store with name '{}' already exists.".format(data['User_Name'])}, 400  )      
        user.save_to_db()
        auth.save_to_db()
        result=User.find_by_name(data['User_Name'])
        team=db.session.query(Team).filter(Team.Team_Name.like(Team_Name))
        for row in team:
            teamid=row.Team_id
            break
        print(teamid)
        userteam=Team_User(teamid,result.User_id)
        db.session.add(userteam)
        db.session.commit()
        cur_user=User.find_by_name(data['User_Name'])
        return prepare_response( cur_user.json(), 201)
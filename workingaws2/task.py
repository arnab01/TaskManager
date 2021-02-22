#!/usr/bin/env/ python3
from db import db
from flask import jsonify
from flask_restful import Resource,reqparse
from sqlalchemy import create_engine
from flask_jwt import jwt_required
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from user import prepare_response

Base=automap_base()

class Task(db.Model):
    __tablename__ = 'Tasks'
    __table__ = db.Table('Tasks', Base.metadata,
                    autoload=True, autoload_with=db.engine)

    def __init__(self,Task_id,Title,Description,Priority,Planned_Date,Assignee,Reporter,Status,Team_Name):
        self.Task_id=Task_id
        self.Title=Title
        self.Description=Description
        self.Priority=Priority
        self.Planned_Date=Planned_Date
        self.Assignee=Assignee
        self.Reporter=Reporter
        self.Status=Status
        self.Team_Name=Team_Name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'Task_id':self.Task_id, 'Title': self.Title,'Description': self.Description,'Priority': self.Priority,'Assignee':self.Assignee,'Reporter':self.Reporter,'Status':self.Status,'Team_Name':self.Team_Name}

    @classmethod
    def find_by_name(cls, Title):
        print(Title)
        val= cls.query.filter_by(Title=Title).first()
        print(val)
        return val

    @classmethod
    def find_by_id(cls, Task_id):
        val= cls.query.filter_by(Task_id=Task_id).first()
        print(val)
        return val
    

    @classmethod
    def find_by_team(cls, Team_Name):
        print(Team_Name)
        val= cls.query.filter_by(Team_Name=Team_Name).first()
        print(val)
        return val

class CreateTask(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('User_Name',
                        type=str,
                        required=True,
                        help="here field cannot be blank."
                        )
    parser.add_argument('Title',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('Description',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('Priority',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('Planned_Date',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('Assignee',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('Reporter',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('Status',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('Team_Name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    @jwt_required()
    def post(self):
        data =CreateTask.parser.parse_args()
        task=Task(None,data['Title'],data['Description'],data['Priority'],data['Planned_Date'],data['Assignee'],data['Reporter'],data['Status'],data['Team_Name'])
        if Task.find_by_name(data['Title']):
            return {'message': "A Task with name '{}' already exists.".format(data['Title'])}, 400

        task.save_to_db()
        cur_task=Task.find_by_name(data['Title'])
        val=str(cur_task.Planned_Date)
        return prepare_response({'Task_id':cur_task.Task_id, 'Title': cur_task.Title,'Description':cur_task.Description,'Priority': cur_task.Priority,'Planned_Date':val,'Assignee':cur_task.Assignee,'Reporter':cur_task.Reporter,'Status':cur_task.Status,'Team_Name':cur_task.Team_Name,'User_Name': cur_task.User_Name}, 201)

class PutStatus(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Status',
                        type=str,
                        required=True,
                        help="status field cannot be blank."
                        )
    @jwt_required()
    def patch(self, Task_id):
        data = PutStatus.parser.parse_args()

        task = Task.find_by_id(Task_id)
        if task:
            task.Status=data['Status']
            task.save_to_db()
            return task.json()
        return prepare_response({'message':'Task_id Doesnt exist'},400)
    @jwt_required()
    def delete(self, Title):
        task = Task.find_by_name(Title)
        if task:
            task.delete_from_db()
            return prepare_response({'message': 'Task deleted.'},200)
        return prepare_response({'message': 'Task not found.'}, 404)

class DeleteTask(Resource):
    @jwt_required()
    def delete(self, Task_id):
        task = Task.find_by_id(Task_id)
        if task:
            task.delete_from_db()
            return prepare_response({'message': 'Task deleted.'},200)
        return prepare_response({'message': 'Task not found.'}, 404)


class GetTask(Resource):
    @jwt_required()
    def get(self,Team_Name):
        tasks=[]
        result = db.session.query(Task).filter(Task.Team_Name.like(Team_Name))
        for row in result:           
            val=str(row.Planned_Date)
            print(val)
            tasks.append({'Task_id':row.Task_id, 'Title': row.Title,'Description': row.Description,'Priority': row.Priority,'Planned_Date':val,'Assignee':row.Assignee,'Reporter':row.Reporter,'Status':row.Status,'Team_Name':row.Team_Name})
        if tasks:
            return prepare_response( tasks,200)
        return prepare_response({'message': 'Team not found'}, 404)

class SortPriority(Resource):
    @jwt_required()
    def get(self,Team_Name):
        tasks=[]
        result = db.session.query(Task).filter(Task.Team_Name.like(Team_Name)).order_by(Task.Priority.desc())
        for row in result:           
            val=str(row.Planned_Date)
            print(val)
            tasks.append({'Task_id':row.Task_id, 'Title': row.Title,'Description': row.Description,'Priority': row.Priority,'Planned_Date':val,'Assignee':row.Assignee,'Reporter':row.Reporter,'Status':row.Status,'Team_Name':row.Team_Name})
        if tasks:
            return prepare_response(tasks,200)
        return prepare_response({'message': 'Team not found'}, 404)

class SortPrioritybyUser(Resource):
    @jwt_required
    def get(self,User_Name):
        tasks=[]
        result = db.session.query(Task).filter(Task.Assignee.like(User_Name)).order_by(Task.Priority.desc())
        for row in result:           
            val=str(row.Planned_Date)
            print(val)
            tasks.append({'Task_id':row.Task_id,'User_Name': row.User_Name, 'Title': row.Title,'Description': row.Description,'Priority': row.Priority,'Planned_Date':val,'Assignee':row.Assignee,'Reporter':row.Reporter,'Status':row.Status,'Team_Name':row.Team_Name})
        if tasks:
            return prepare_response(tasks,200)
        return prepare_response({'message': 'Team not found'}, 404)


class SortPD(Resource):
    @jwt_required()
    def get(self,Team_Name):
        tasks=[]
        result = db.session.query(Task).filter(Task.Team_Name.like(Team_Name)).order_by(Task.Planned_Date)
        for row in result:           
            val=str(row.Planned_Date)
            print(val)
            tasks.append({'Task_id':row.Task_id,'Title': row.Title,'Description': row.Description,'Priority': row.Priority,'Planned_Date':val,'Assignee':row.Assignee,'Reporter':row.Reporter,'Status':row.Status,'Team_Name':row.Team_Name})
        if tasks:
            return prepare_response(tasks,200)
        return prepare_response({'message': 'Team not found'}, 404)

class SortPDbyUser(Resource):
    @jwt_required
    def get(self,User_Name):
        tasks=[]
        result = db.session.query(Task).filter(Task.Assignee.like(User_Name)).order_by(Task.Planned_Date)
        for row in result:           
            val=str(row.Planned_Date)
            print(val)
            tasks.append({'Task_id':row.Task_id, 'Title': row.Title,'Description': row.Description,'Priority': row.Priority,'Planned_Date':val,'Assignee':row.Assignee,'Reporter':row.Reporter,'Status':row.Status,'Team_Name':row.Team_Name})
        if tasks:
            return prepare_response(tasks,200)
        return prepare_response({'message': 'Team not found'}, 404)


class GetUserTask(Resource):
    @jwt_required()
    def get(self,User_Name):
        tasks=[]
        result = db.session.query(Task).filter(Task.Assignee.like(User_Name))
        for row in result:
            val=str(row.Planned_Date)
            print(val)
            tasks.append({'Task_id':row.Task_id,'Title': row.Title,'Description': row.Description,'Priority': row.Priority,'Planned_Date':val,'Assignee':row.Assignee,'Reporter':row.Reporter,'Status':row.Status,'Team_Name':row.Team_Name})
        if tasks:
            return prepare_response(tasks,200)
        return prepare_response({'message': 'Team not found'}, 404)

from db import db
from flask_restful import Resource,reqparse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
Base=automap_base()


class Auth(db.Model):
    __tablename__ = 'auth'
    __table__ = db.Table('auth', Base.metadata,
                    autoload=True, autoload_with=db.engine)

    def __init__(self,id,User_Name,password):
        self.id=id
        self.User_Name=User_Name
        self.password=password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, User_Name):
        print(User_Name)
        val= cls.query.filter_by(User_Name=User_Name).first()
        print(val)
        return val

    @classmethod
    def find_by_id(cls, User_id):
        print(User_id)
        val= cls.query.filter_by(id=User_id).first()
        print(val)
        return val

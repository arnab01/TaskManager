#!/usr/bin/env/ python3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
Base=automap_base()
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://admin:12345678@mysql-dbms.cjxt3oa51lw1.ap-south-1.rds.amazonaws.com/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
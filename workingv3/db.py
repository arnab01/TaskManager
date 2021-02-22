from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
Base=automap_base()
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:vishal@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
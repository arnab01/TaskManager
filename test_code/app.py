from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_restful import Resource, reqparse
from flask_mysqldb import MySQL
from security import authenticate,identity
from user import UserRegister
app=Flask(__name__)

app.secret_key = 'trial'
api = Api(app)

jwt = JWT(app, authenticate, identity )
api.add_resource(UserRegister, '/register')
    
if __name__ == '__main__':
    app.run(debug=True)
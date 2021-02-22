from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from flask_mysqldb import MySQL
app = Flask(__name__)

""" app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "vishal"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_DB'] = "mydb"
app.config['MYSQL_CURSORCLASS'] = "DictCursor" """

#mysql=MySQL(app)
def authenticate(username, password):
    user = {
        "id":1,
        "username": "vishalmk",
        "password": "vishal"
    }
    if user and safe_str_cmp(user[password],password):
        return user


app.secret_key = 'trial'
#api = Api(app)

jwt = JWT(app, authenticate )



    
if __name__ == '__main__':
    app.run(debug=True)

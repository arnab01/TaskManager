from flask import Flask
from flask_restful import Resource, reqparse
from flask_mysqldb import MySQL
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp
from flask_restful import Api
app = Flask(__name__)
app.secret_key = 'trial'
api = Api(app)
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "vishal"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_DB'] = "mydb"
app.config['MYSQL_CURSORCLASS'] = "DictCursor" 

mysql=MySQL(app)    
data={
    "id":8,
    "username":"hii",
    "password":"pasks"
}
def authenticate(username, password):
    if  safe_str_cmp(data['password'], password):
        return data


def identity(payload):
    user_id = payload['identity']
    if  safe_str_cmp(data['id'], user_id):
        return user_id 
""" @app.route('/')
def func():
    cur=mysql.connection.cursor()

    query = "INSERT INTO auth(User_Name,password,User_id) VALUES ( %s, %s, %s)"
    cur.execute(query, (data['username'], data['password'],data['id']) )
    mysql.connection.commit()
    cur.close()
    return 'done!' """
 

class UserRegister(Resource):
    TABLE_NAME = 'user'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):    
        cursor = mysql.connection.cursor()

        query = "INSERT INTO auth VALUES (%s,%s,%s)"
        cursor.execute(query, (data['username'], data['password'],data['id']))

        cursor.connection.commit()
        cursor.close()

        return {"message": "User created successfully."}, 201

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)
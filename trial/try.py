from flask import Flask
from flask_restful import Resource, reqparse
from flask_mysqldb import MySQL
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp
from flask_restful import Api

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "vishal"

app.config['MYSQL_DB'] = "mydb"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql=MySQL(app)

app.secret_key = 'trial'
api = Api(app)

def authenticate(User_Name, password):
    user = User.find_by_User_Name(User_Name)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id) 
class User():
    TABLE_NAME = 'auth'

    def __init__(self, _id, User_Name="", password=""):
        self.id = _id
        self.User_Name = User_Name
        self.password = password

    @classmethod
    def find_by_User_Name(cls, User_Name):
        cur=mysql.connection.cursor()
        cur.execute("select * from auth where User_Name=%s",(User_Name,))
       
        row = cur.fetchall()
        if row:
            user = cls(*row)
        else:
            user = None

        cur.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        cur=mysql.connection.cursor()

        query = "SELECT * FROM {table} WHERE User_id=?".format(table=cls.TABLE_NAME)
        cur.execute(query, (_id,))
        row = cur.fetchall()
        if row:
            user = cls(*row)
        else:
            user = None

        cur.close()
        return user 


class UserRegister(Resource):
    TABLE_NAME = 'auth'
    parser = reqparse.RequestParser()
    parser.add_argument('User_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('User_Name',
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
        data = UserRegister.parser.parse_args()

        if User.find_by_User_Name(data['User_Name']):
            return {"message": "User with that User_Name already exists."}, 400

        
        cursor = mysql.connection.cursor()

        query = "INSERT INTO auth VALUES (%s,%s,%s)"
        cursor.execute(query, (data['User_Name'], data['password'],data['User_id']))

        cursor.connection.commit()
        cursor.close()

        return {"message": "User created successfully."}, 201

jwt = JWT(app, authenticate, identity )
api.add_resource(UserRegister, '/register')
    
if __name__ == '__main__':
    app.run(debug=True)
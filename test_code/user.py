from flask import Flask
from flask_restful import Resource, reqparse
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql=MySQL(app)
""" app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "vishal"

app.config['MYSQL_DB'] = "mydb"
app.config['MYSQL_CURSORCLASS'] = "DictCursor" """



class User():
    TABLE_NAME = 'auth'

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        cur=mysql.connection.cursor()
        result=cur.execute("select * from auth where User_Name=?",(username,))
       
        row = result.fetchone()
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
        result = cur.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        cur.close()
        return user 


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
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        
        cursor = mysql.connection.cursor()

        query = "INSERT INTO auth VALUES ( ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (data['username'], data['password']))

        cursor.commit()
        cursor.close()

        return {"message": "User created successfully."}, 201
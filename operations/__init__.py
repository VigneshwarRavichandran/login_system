from flask import jsonify
import secrets
from flask_mysqldb import MySQL

class Operate():
    def __init__(self, app):
        # Config MySQL
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = '1998'
        app.config['MYSQL_DB'] = 'login_system'
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        app.config['SECRET_KEY'] = 'ahjcusyxduywduyfuy41276re46wfqsuq'
        self.app = app
        # init MYSQL
        self.mysql = MySQL(self.app)


    def create_user(self, username, password):
        cur = self.mysql.connection.cursor()
        access_token = secrets.token_urlsafe(20)
        cur.execute("INSERT INTO user_details(username, password, token) VALUES(%s, %s, %s)", (username, password, access_token, ))
        cur.execute("INSERT INTO user_token(token) VALUES(%s)", (access_token, ))
        self.mysql.connection.commit()
    	
    def existing_username(self, username):
        cur = self.mysql.connection.cursor()
        result = cur.execute("SELECT * FROM user_details WHERE username = %s", (username, ))
        if result == 0:
            return False
        else:
            return True

    def existing_user(self, username, password):
        cur = self.mysql.connection.cursor()
        result = cur.execute("SELECT * FROM user_details WHERE username = %s AND password = %s", (username, password, ))
        if result == 0:
            return False
        else:
            return True

    def get_token(self, username, password):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT token FROM user_details WHERE username = %s AND password = %s", (username, password, ))
        return(cur.fetchone())

    def existing_token(self, user_token):
        cur = self.mysql.connection.cursor()
        result = cur.execute("SELECT * FROM user_token WHERE token= %s", (user_token, ))
        if result == 0:
            return False
        else:
            return True

    def get_content(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM country_details")
        return(cur.fetchall())

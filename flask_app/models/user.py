from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re    #this imports the regex module
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile(r'^(?=.[a-z])(?=.[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
db = "recipes"

class User:
    def __init__( self, db_data ):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.users=[]


    @staticmethod
    def validate_register(user):
        is_valid = True # we assume this is true
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        if len(results) >= 1:
            flash ("Email is already in use", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email.", "register")
            is_valid= False
        if len(user['first_name']) < 3:
            flash ("First name must be at least 3 characters", "register")
            is_valid=False
        if len(user['last_name']) < 3:
            flash ("Last name must be at least 3 characters", "register")
            is_valid=False
        if user['password'] != user['confirm']:
            flash ("Passwords Do Not Match", "register")
            is_valid=False
        return is_valid


    @classmethod
    def save( cls , data ):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query,data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        login_and_registration = connectToMySQL(db).query_db(query)
        users =[]
        for user_info in login_and_registration:
            users.append(cls(user_info))
        return users


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])


    @classmethod 
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

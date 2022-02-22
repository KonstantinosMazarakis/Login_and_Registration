from asyncio.windows_events import NULL
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z])[a-zA-Z\d]{8,45}$')
FIRST_LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]{2,45}$')


class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.gender = data['gender']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, gender, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(gender)s, %(email)s, %(password)s ,NOW() , NOW())"
        results = connectToMySQL('login_and_registration_schema').query_db( query, data )
        return results

    @classmethod
    def login(cls,data):
        query = "SELECT * from users WHERE email = %(email)s"
        results = connectToMySQL('login_and_registration_schema').query_db( query, data )
        if len(results) < 1:
            return False
        return User(results[0])



    @staticmethod
    def validate_user(user):
        is_valid = True
        if not FIRST_LAST_NAME_REGEX.match(user['first_name']):
            flash("First name must be at least 2 characters and only letters.", 'create_user')
            is_valid = False
        if not FIRST_LAST_NAME_REGEX.match(user['last_name']):
            flash("Last name must be at least 2 characters and only letters.", 'create_user')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'create_user')
            is_valid = False
        if User.login(user) != False:
            flash("Email address already exist!", 'create_user')
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash("Passwords must have a least 1 number and 1 uppercase letter and minimum of 8 digits length", 'create_user')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Password and Confirm Password has to be the same", 'create_user')
            is_valid = False
        return is_valid
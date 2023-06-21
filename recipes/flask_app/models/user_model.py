from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_email(cls,data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod
    def validator(data):
        is_valid = True
        if len(data['first_name']) < 1:
            is_valid = False
            flash('First name required', 'reg')
        elif len(data['first_name']) < 2:
            is_valid = False
            flash('First name must be at least 2 chars', 'reg')
        elif not ALPHA.match(data['first_name']):
            is_valid = False
            flash('First name must be letter only', 'reg')
        if len(data['last_name']) < 1:
            is_valid = False
            flash('Last name required', 'reg')
        elif len(data['last_name']) < 2:
            is_valid = False
            flash('Last name must be at least 2 chars', 'reg')
        elif not ALPHA.match(data['last_name']):
            is_valid = False
            flash('Last name must be letter only', 'reg')
        if len(data['email']) < 1:
            is_valid = False
            flash('Email required', 'reg')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Email must be valid format','reg')
        else:
            # user_data = {
            #     'email': data['email']
            # }
            # 2 ways to do this.  you can put the user_data dict in there
            # or you can just put {'email': data['email']} into it
            potential_user = User.get_by_email({'email': data['email']})# this will return a user or False
            if potential_user:
                flash('email already exists in db (hope that was you)', 'reg')
                is_valid = False
        if len(data['password']) < 1:
            flash('pass req', 'reg')
            is_valid = False
        elif len(data['password']) < 8:
            flash('pass must be > 8 char', 'reg')
            is_valid = False
        elif data['password'] != data['confirm_pass']:
            flash('passwords must match', 'reg')
            is_valid = False
        return is_valid
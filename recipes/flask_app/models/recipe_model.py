from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash
import re
ALPHA = re.compile(r"^[a-zA-Z]+$")
ALPHAspace = re.compile(r"^[a-zA-Z ]+$")

class Recipe:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.datemade = data['datemade']
        self.under30min = data['under30min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes').query_db(query)
        # Create an empty list to append our instances of ninjas
        print('------------>>>>>>>>>>>>>', results)
        all_recipes = []
        # Iterate over the db results and create instances of ninjas with cls.
        if results:
            for row in results:
                this_recipe = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_recipe.user = this_user
                all_recipes.append(this_recipe)
        return all_recipes
    
    @classmethod
    def get_one(cls, user_id):
        query  = "SELECT * FROM recipes WHERE id = %(id)s;"
        data = {'id':ninja_id}
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)
        return cls(results[0]) 
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        # the_recipe=[]
        if results:
            this_recipe = cls(results[0])
            user_data = {
                **results[0],
                'id': results[0]['users.id'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at']
                }
            this_user = user_model.User(user_data)
            this_recipe.user = this_user
            # the_recipe.append(this_recipe)
            return this_recipe
        return False
    
    @classmethod
    def save(cls, data ):
        query = """INSERT INTO recipes ( name , description, instructions, under30min, datemade, created_at, updated_at, user_id) VALUES ( %(name)s , %(description)s , %(instructions)s , %(under30min)s , %(datemade)s , NOW(), NOW(), %(user_id)s );"""
        # data is a dictionary that will be passed into the save method 
        return connectToMySQL('recipes').query_db( query, data )
    
    @classmethod
    def update(cls,data):
        query = """UPDATE recipes SET name=%(name)s,description=%(description)s, instructions=%(instructions)s, under30min=%(under30min)s,datemade=%(datemade)s,updated_at=NOW() WHERE id = %(id)s;"""
        print('\n'*5)
        print(query)
        print(data)
        print('test')
        return connectToMySQL('recipes').query_db(query,data)
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        # data = {"id": 'id'}
        print('heeeeeeee')
        print(data)
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validator(data):
        is_valid = True
        if len(data['name']) < 1:
            is_valid = False
            flash('Name required')
        elif len(data['name']) < 3:
            is_valid = False
            flash('Name must be at least 3 chars')
        elif not ALPHAspace.match(data['name']):
            is_valid = False
            flash('Name must be letter only')
        if len(data['description']) < 1:
            is_valid = False
            flash('Description required')
        elif len(data['description']) < 3:
            is_valid = False
            flash('Description must be at least 3 chars')
        if len(data['instructions']) < 1:
            is_valid = False
            flash('Instructions required')
        elif len(data['instructions']) < 3:
            is_valid = False
            flash('Instructions must be at least 3 chars')
        if len(data['datemade']) < 1:
            is_valid = False
            flash('Date made is required')
        # if len(data['under30min']) < 1:
        if ('under30min' not in data):
            is_valid = False
            flash('Under 30 minutes(yes/no) required')
        return is_valid
        # if len(data['password']) < 1:
        #     flash('pass req', 'reg')
        #     is_valid = False
        # elif len(data['password']) < 8:
        #     flash('pass must be > 8 char', 'reg')
        #     is_valid = False
        # elif data['password'] != data['confirm_pass']:
        #     flash('passwords must match', 'reg')
        #     is_valid = False
        # return is_valid
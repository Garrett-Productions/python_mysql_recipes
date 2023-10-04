from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash
import re 
db = "recipes"

class Recipe:
    def __init__( self, db_data ):
        self.id = db_data['id']
        self.user_id = db_data['user_id'] #foreign key
        self.name = db_data['name']
        self.description = db_data['description']
        self.instructions = db_data['instructions']
        self.under_30 = db_data['under_30']
        self.date_made = db_data['date_made']
        self.creator = None #kind of like our empty list
        self.likes = []
        # self.kept_recipes = []
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True #if validations fail set is_valid = False
        if len(recipe['name']) < 3:
            flash ("Recipe name must be 3 characters or longer", "recipe")
            is_valid=False
        if len(recipe['description']) < 3:
            flash ("Must include a description", "recipe")
            is_valid=False
        if len(recipe['instructions']) < 3:
            flash ("Instructions field must not be blank", "recipe")
            is_valid=False
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (user_id, name, description, instructions, under_30, date_made) VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def insert_like(cls,data):
        query = "INSERT INTO likes(user_id, recipe_id) VALUES(%(user_id)s, %(recipe_id)s)"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def deselect_like(cls,data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND recipe_id = %(recipe_id)s"
        return connectToMySQL(db).query_db(query,data)
    
    #lets try this method in cars, but try it in sql first
    @classmethod
    def get_with_likes(cls,id):
        query = """
            SELECT * FROM recipes 
            LEFT JOIN likes ON recipes.id = likes.recipe_id
            LEFT JOIN users ON likes.user_id = users.id
            JOIN users AS creator ON recipes.user_id = creator.id
            WHERE recipes.id = %(id)s; 
            """

        results = connectToMySQL(db).query_db(query, {'id':id})
        if results: #if we get results back set a row equal to a variables
            recipe = cls(results[0])
            
            recipe.creator = user.User({
                'id': results[0]['creator.id'],
                'first_name': results[0]['creator.first_name'],
                'last_name': results[0]['creator.last_name'],
                'email':results[0]['creator.email'],
                'password':results[0]['creator.password'],
                'created_at': results[0]['creator.created_at'],
                'updated_at': results[0]['creator.updated_at']
                })

            for result in results:
                if result['likes.user_id']: #making sure our users id has something in it
                    recipe.likes.append(user.User({
                        'id': result['users.id'],
                        'first_name': result['first_name'],
                        'last_name': result['last_name'],
                        'email':result['email'],
                        'password':result['password'],
                        'created_at': result['users.created_at'],
                        'updated_at': result['users.updated_at']
                    }))
            return recipe
        return None #if returns none we know theres an issue, we should be getting back that row
    
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id WHERE user_id = users.id;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])


    @classmethod
    def get_all(cls):
        query = '''
                SELECT * FROM recipes 
                JOIN users on recipes.user_id = users.id 
                LEFT JOIN likes ON recipes.id = likes.recipe_id
                ;'''
        results = connectToMySQL(db).query_db(query)
        recipe_list =[]
        print(recipe_list)
        for row in results:
            if recipe_list and row['id'] == each_recipe.id: 
                each_recipe.likes.append(row['likes.user_id'])
            else:
                each_recipe = cls(row)
                user_data = {
                    "id": row['users.id'],
                    "first_name" : row['first_name'],
                    "last_name" : row['last_name'],
                    "email" : row['email'],
                    "password" : row['password'],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at']
                }
                each_recipe.creator = user.User(user_data)
                print(each_recipe.creator)
                if row['likes.user_id'] != None:
                    each_recipe.likes.append(row['likes.user_id'])
                recipe_list.append(each_recipe)
        return recipe_list

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id WHERE recipes.id = %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        user_data = {
                "id": results[0]['users.id'],
                "first_name" : results[0]['first_name'],
                "last_name" : results[0]['last_name'],
                "email" : results[0]['email'],
                "password" : results[0]['password'],
                "created_at" : results[0]['users.created_at'],
                "updated_at" : results[0]['users.updated_at']
            }
        one_recipe = cls(results[0])
        one_recipe.creator = user.User(user_data)
        return one_recipe


    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET user_id=%(user_id)s, name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_30=%(under_30)s, date_made=%(date_made)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    # @classmethod
    # def keep_recipe(cls,data):
    #     query = "INSERT INTO kept_recipes (user_id, recipe_id) VALUES (%(user_id)s, %(recipe_id)s)"
    #     return connectToMySQL(db).query_db(query,data)  

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
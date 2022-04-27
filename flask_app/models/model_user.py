from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_location

from flask_app import DATABASE, bcrypt

from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.locations = []

    @property
    def fullname(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    @classmethod
    def register_user(cls, data: dict) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id


    @classmethod
    def get_all_users_db(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)#
        
        if results: 
            all_users = []
            for user in results:
                user_actual = cls(user)
                all_users.append(user_actual)
            return all_users
        return []

    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        user_result = connectToMySQL(DATABASE).query_db(query, data)
        if user_result:
            one_user = (cls(user_result[0]))
            return one_user
        return False


    @classmethod
    def get_one_by_email(cls, data:dict) -> object:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            user_actual = cls(result[0])
            return user_actual
        return False


    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        users_result = connectToMySQL(DATABASE).query_db(query)
        all_users = []
        for user in users_result:
            all_users.append(user)
        return all_users


    @classmethod
    def get_user_with_locations(cls, data):
        query = "SELECT * FROM users LEFT JOIN locations ON locations.user_id = users.id WHERE users.id = %(id)s;"
        location_id_result = connectToMySQL(DATABASE).query_db(query, data)
        spot = cls(location_id_result[0])
        for row_from_db in location_id_result:

            location_data = {
                "id": row_from_db["locations.id"],
                "name": row_from_db["name"],
                "created_at": row_from_db["locations.created_at"],
                "updated_at": row_from_db["locations.updated_at"],
                "user_id": row_from_db["locations.user_id"],
            }
            User.locations.append(model_location.Location(location_data))
        return spot

########### VALIDATION

    @staticmethod
    def validator(form_data:dict):
            is_valid = True

            if len(form_data['first_name']) < 2:
                flash("First name is required!", 'err_first_name')
                is_valid = False

            if len(form_data['last_name']) < 2:
                flash("Last name is required!", 'err_last_name')
                is_valid = False

            if len(form_data['email']) <= 0:
                flash("Email is required!", 'err_email')
                is_valid = False
            elif not EMAIL_REGEX.match(form_data['email']): 
                flash("Invalid email address!", 'err_email')
                is_valid = False

            if len(form_data['password']) < 8:
                flash("Password must be at least 8 characters long!", 'err_password')
                is_valid = False
            if len(form_data['password_confirmation']) < 8:
                flash("Password must be at least 8 characters long!", 'err_password_confirmation')
                is_valid = False
            if (form_data['password'] != form_data['password_confirmation']):
                flash("Passwords must be the same!", 'err_password_confirmation')
                is_valid = False
            return is_valid


    @staticmethod
    def validator_login(form_data:dict):
        is_valid = True
        if len(form_data['email']) < 2:
            flash("Email is required!", 'err_email_login')
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", 'err_email_login')
            is_valid = False

        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters long!", 'err_password_login')
            is_valid = False
        else:
            potential_user = User.get_one_by_email({'email': form_data['email']})
            print(potential_user)
            if potential_user == False:
                flash("Invalid Credentials!", 'err_email_login')
                is_valid = False
            else:
                print(potential_user)
                print(form_data)
                if not bcrypt.check_password_hash(potential_user.password, form_data['password']):
                    flash("Invalid Credentials!", 'err_password_login')
                    is_valid = False
                else:
                    session['uuid'] = potential_user.id

        return is_valid


# save || create
# get_all
# get_one
# update_one
# delete_one
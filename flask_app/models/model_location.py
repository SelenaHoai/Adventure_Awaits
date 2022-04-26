from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user

from flask_app import DATABASE, bcrypt

from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Location:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.favorite = data['favorite']
        self.visit = data['visit']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @property
    def user_actual(self):
        return model_user.User.get_one_location({'id': self.user_id})


    @classmethod
    def create_one_location(cls, data):
        query = "INSERT into locations (name, favorite, visit, user_id) VALUES (%(name)s, %(favorite)s, %(visit)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_one_location(cls, data):
        query = "SELECT * FROM locations WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all_locations(cls, data):
        query = "SELECT * FROM locations LEFT JOIN users ON locations.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        
        if results: 
            all_locations = []
            for location in results:
                location_actual = cls(location)

                data = {
                    'id': location['users.id'],
                    'first_name': location['first_name'],
                    'last_name': location['last_name'],
                    'email': location['email'],
                    'password': location['password'],
                    'created_at': location['users.created_at'],
                    'updated_at': location['users.updated_at'],
                }

                owner = model_user.User(data)
                location_actual.owner = owner

                all_locations.append(location_actual)
            return all_locations
        return []

    # @classmethod
    # def update_one_location(cls, data: dict) -> object:
    #     query = "UPDATE locations SET location=%(location)s, description=%(description)s, date=%(date)s, number=%(number)s WHERE id = (%(id)s);"
    #     return connectToMySQL(DATABASE).query_db(query, data)
    
    
    # @classmethod
    # def delete_location(cls, data: dict) -> object:
    #     query = "DELETE FROM locations WHERE id = (%(id)s);"
    #     return connectToMySQL(DATABASE).query_db(query, data)


########## VALIDATION

    # @staticmethod
    # def validator(form_data:dict):
    #         is_valid = True

    #         if len(form_data['name']) < 3:
    #             flash("Name is required!", 'err_name')
    #             is_valid = False

    #         if len(form_data['description']) < 3:
    #             flash("Description is required!", 'err_description')
    #             is_valid = False

    #         if form_data['date'] == "":
    #             flash("Date is required!", 'err_date')
    #             is_valid = False

    #         if "number" not in form_data:
    #             flash("Number is required!", 'err_number')
    #             is_valid = False

    #         return is_valid
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user, model_attraction

from flask_app import DATABASE, bcrypt

from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Location:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.attractions = []


    @property
    def user_actual(self):
        return model_user.User.get_one_location({'id': self.user_id})


    @classmethod
    def save(cls, data):
        query = "INSERT into locations (name, user_id) VALUES (%(name)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_all_by_user_id(cls, data):
        query = "SELECT * FROM locations LEFT JOIN attractions ON attractions.location_id = locations.id WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        locations = []
        for row in results:
            if len(locations) == 0 or locations[-1].id != row['id']:
                locations.append(cls(row))
            attr_data = {
                "id": row['attractions.id'],
                "name": row['attractions.name'],
                "created_at": row['attractions.created_at'],
                "updated_at": row['attractions.updated_at'],
                "location_id": row['id']
            }
            locations[-1].attractions.append(model_attraction.Attraction(attr_data))

        return locations

    @classmethod
    def get_all_joined(cls, data):
        query = "SELECT * FROM locations LEFT JOIN attractions ON attractions.location_id = locations.id WHERE locations.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query)
        location = cls(results[0])
        for row in results:
            attr_data = {
                "id": row['attractions.id'],
                "name": row['attractions.name'],
                "created_at": row['attractions.created_at'],
                "updated_at": row['attractions.updated_at'],
                "location_id": row['id']
            }
            location.attractions.append(model_attraction.Attraction(attr_data))
        return location


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
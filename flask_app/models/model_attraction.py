from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user, model_location

from flask_app import DATABASE, bcrypt

from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Attraction:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location_id = data['location_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM attractions"
        results = connectToMySQL(DATABASE).query_db(query)
        attractions = []
        for attraction in results:
            attractions.append(cls(attraction))
        return attractions

    @classmethod
    def save_mult(cls, data, loc_id):
        # newData = {
        #     data,
        #     "morelines": cls.add_more_values(data, loc_id)
        # }
        test = cls.add_more_values(data, loc_id)
        query = f"INSERT INTO attractions (name, location_id) VALUES {test};"
        return connectToMySQL(DATABASE).query_db(query)
    
    @classmethod
    def save_one(cls, data):
        query = f"INSERT INTO attractions (name, location_id) VALUES (%(name)s, %(loc_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def add_more_values(data, loc_id):
        more_values_str = ""
        results = data.to_dict(flat=False)
        for i, name in enumerate(results['name']):
            if i == len(results['name']) - 1:
                more_values_str += f"('{name}', {loc_id})"
            else:
                more_values_str += f"('{name}', {loc_id}), "

        return more_values_str

    @classmethod
    def update_attractions(cls, data: dict) -> object:
        query = "UPDATE attractions SET name=%(name)s WHERE id = (%(id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def separate_keys(data):
        sep_data = {
            "update": [],
            "new": []
        }
        for key in data:
            sep_list = key.split("_")
            if sep_list[0] == "name":
                if sep_list[1] != "new":
                    new_item = {
                        "name": data[key],
                        "id": sep_list[1]
                    }
                    sep_data["update"].append(new_item)            
        new_data = data.to_dict(flat=False)
        if "name_new" in new_data:
            sep_data["new"] = new_data["name_new"]
        return sep_data

    @classmethod
    def delete_attraction(cls, data: dict) -> object:
        query = "DELETE FROM attractions WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
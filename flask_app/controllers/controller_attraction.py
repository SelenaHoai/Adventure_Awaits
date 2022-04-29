from flask_app import app, bcrypt
from flask import render_template, request, redirect, session


from flask_app.models import model_user, model_location, model_attraction


# ******************** DISPLAY ROUTE **********************

@app.route('/attractions/delete/<int:id>/<int:locid>')
def attraction_delete(id,locid):
    data = {
        "id": id
    }
    model_attraction.Attraction.delete_attraction(data)
    return redirect(f"/locations/edit/{locid}")
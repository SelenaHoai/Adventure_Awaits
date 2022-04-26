from flask_app import app, bcrypt
from flask import render_template, request, redirect, session


from flask_app.models import model_user, model_location


# ******************** DISPLAY ROUTE **********************

@app.route('/locations/new')
def locations_new():
    if 'uuid' in session:
        create_one_location = model_location.Location.get_all_locations({'id':session['uuid']})
        all_users_from_db = model_location.Location.get_all_locations({'id':session['uuid']})
    if not 'uuid' in session:
        return render_template("add_location.html")
    return render_template("add_location.html", user=all_users_from_db, location=create_one_location)


# @app.route('/locations/<int:id>')
# def location_descriptions(id):
#     if not 'uuid' in session:
#         return redirect('/')
#     data = {
#         "id": id
#     }
#     user_from_db = model_user.User.get_one_user({'id':session['uuid']})
#     get_one_location=model_location.Location.get_one_location(data)
#     return render_template("location_descriptions.html", location=get_one_location, user=user_from_db)


# @app.route('/locations/edit/<int:id>')
# def location_edit(id):
#     if not 'uuid' in session:
#         return redirect('locations/create')
#     data = {
#         "id": id
#     }
#     user_from_db = model_user.User.get_one_user({'id':session['uuid']})
#     edit_one_location = model_location.Location.get_one_location(data)
#     return render_template("location_edit.html", location=edit_one_location, user=user_from_db)


@app.route('/locations/delete/<int:id>')
def location_delete(id):
    data = {
        "id": id
    }
    model_location.Location.delete_location(data)
    return redirect("/user/dashboard")






# ******************** ACTION ROUTE **********************

@app.route('/locations/create', methods=['post'])
def locations_create(): 
    is_valid = model_location.Location.validator(request.form)
    if not is_valid:
        return redirect('/locations/new')
    user_data = {
        "user_id": session["uuid"],
        "location": request.form["location"],   
        "description": request.form["description"],     
        "date": request.form["date"],
        "number": request.form["number"]
    }
    model_location.Location.create_one_location(user_data)
    return redirect("/user/dashboard")


@app.route('/locations/update/<int:id>', methods=['post'])
def location_update(id):
    is_valid = model_location.Location.validator(request.form)
    if not is_valid:
        return redirect(f'/locations/edit/{id}')
    data = {
        **request.form,
        "id": id,
        "user_id":session['uuid']
    }
    model_location.Location.update_one_location(data)
    return redirect("/user/dashboard")


# ************************* Keep This At The Bottom ************************

if __name__ == "__main__":
    app.run(debug=True)

# **************************** END
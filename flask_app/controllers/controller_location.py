from flask_app import app, bcrypt
from flask import render_template, request, redirect, session


from flask_app.models import model_user, model_location, model_attraction


# ******************** DISPLAY ROUTE **********************

@app.route('/locations/new')
def loc_att_new():
    if not 'uuid' in session:
        return redirect('/')
    return render_template("location_add.html")


# @app.route('/locations/edit/<int:id>')
# def loc_att_edit(id):
#     return render_template('location_update.html')


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


@app.route('/locations/edit/<int:id>')
def location_edit(id):
    if not 'uuid' in session:
        return redirect('/')
    data = {
        "id": id
    }
    user_from_db = model_user.User.get_one_user({'id':session['uuid']})
    edit_one_location = model_location.Location.get_all_joined(data)
    return render_template("location_update.html", location=edit_one_location, user=user_from_db)


@app.route('/locations/delete/<int:id>')
def location_delete(id):
    data = {
        "id": id
    }
    model_location.Location.delete_location(data)
    return redirect(f"/locations/edit/{id}")




# ******************** ACTION ROUTE **********************

@app.route('/locations/create', methods=['post'])
def loc_att_create(): 
    loc_id = model_location.Location.save({ 'name': request.form['l_name'], 'user_id': 1 })
    model_attraction.Attraction.save_mult(request.form,loc_id)
    return redirect("/user/dashboard")


@app.route('/locations/update/<int:id>', methods=['post'])
def location_update(id):
    model_location.Location.update_one_location({ 'name': request.form['l_name'], 'id': id })
    sep_list = model_attraction.Attraction.separate_keys(request.form)
    for item in sep_list["update"]:
        model_attraction.Attraction.update_attractions(item)
    for item in sep_list["new"]:
        new_attr={
            "name": item,
            "loc_id": id
        }
        model_attraction.Attraction.save_one(new_attr)
    return redirect("/user/dashboard")


# ************************* Keep This At The Bottom ************************

# if __name__ == "__main__":
#     app.run(debug=True)

# **************************** END
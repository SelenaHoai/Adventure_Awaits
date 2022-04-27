from flask_app import app, bcrypt
from flask import render_template, request, redirect, session


from flask_app.models import model_user, model_location



# ******************** DISPLAY ROUTE **********************

@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/user/dashboard')
def dashboard_for_user():
    if 'uuid' in session:
        all_locations_from_db = model_location.Location.get_all_by_user_id({'user_id':session['uuid']})
        user_from_db = model_user.User.get_one_user({'id':session['uuid']})
        return render_template('dashboard_user.html', all_locations=all_locations_from_db, user=user_from_db)
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    return redirect('/')


# ******************** ACTION ROUTE **********************

@app.route('/process/login', methods=['post'])
def process_login():
    # validate login
    is_valid = model_user.User.validator_login(request.form)
    if not is_valid:
        return redirect('/login')
    return redirect('/user/dashboard')



@app.route('/process/register', methods=['post'])
def process_register():
    # validate user
    is_valid = model_user.User.validator(request.form)
    if not is_valid:
        return redirect('/process/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        **request.form,
        'password': pw_hash
    }
    id = model_user.User.register_user(data)
    session['uuid'] = id
    return redirect('/user/dashboard')

# ************************* Keep This At The Bottom *************************

# if __name__ == "__main__":
#     app.run(debug=True)

# **************************** END
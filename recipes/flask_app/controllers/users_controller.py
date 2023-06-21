from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User

bcrypt = Bcrypt(app)

# Home page

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/recipes')
    return render_template('index.html')

# register route

@app.route('/users/register', methods=['POST'])
def reg_user():
    print('\n'*4)
    print(request.form)
    if not User.validator(request.form):
        return redirect('/')
    
    # hash the password
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pass,
        'confirm_pass': hashed_pass
    }
    logged_user_id = User.create(data)
    session['user_id'] = logged_user_id
    return redirect('/recipes')

# login route

@app.route('/users/login', methods=['POST'])
def log_user():
    data = {
        'email': request.form['email']
    }
    potential_user = User.get_by_email(data)
    if not potential_user:
        flash('Invalid credentials', 'log')
        return redirect('/')
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash('Invalid credentials', 'log')
        return redirect('/')
    session['user_id'] = potential_user.id
    return redirect('/')

# logout route

@app.route('/users/logout')
def logout():
    del session['user_id']
    return redirect('/')
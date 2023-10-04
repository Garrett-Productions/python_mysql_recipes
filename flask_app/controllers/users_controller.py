from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.controllers import recipes_controller
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime
realdate = '%d-%m-%Y'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/recipes')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("invalid Password", "login")
        return redirect ('/')
    session['user_id'] = user.id
    return redirect('/recipes')

@app.route('/user/<int:id>')
def logged_recipes(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    user=User.get_by_id(data)
    return render_template("liked_recipes.html", recipes = Recipe.get_liked_recipes(id), user = user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
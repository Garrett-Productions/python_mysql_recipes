from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.controllers import users_controller
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime
realDate = '%d-%m-%Y'

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template("recipes.html", user=User.get_by_id(data), all_recipes = Recipe.get_all(), dtformat=realDate) 


@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template("add_recipe.html", user=User.get_by_id(data))


@app.route('/create_recipe', methods = ['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "user_id": session['user_id'],
        "name":request.form['name'],
        "description":request.form['description'], 
        "instructions":request.form['instructions'], 
        "date_made":request.form['date_made'],
        "under_30":request.form['under_30'] #left side is what is in our database
    }
    Recipe.save(data)
    return redirect("/recipes")


@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout') #i need to fix these validations and edit my stuff and dsubmit the assignemnt 
    data = {
        "id": session['user_id']
    }
    recipe_data = {
        "id": id
    }
    return render_template("edit_recipe.html", user=User.get_by_id(data), one_recipe= Recipe.get_by_id(recipe_data))

@app.route('/update_recipe/<int:id>', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')
    recipe_data = {
        "id": id,
        "user_id": session['user_id'],
        "name":request.form['name'],
        "description":request.form['description'], 
        "instructions":request.form['instructions'], 
        "date_made":request.form['date_made'],
        "under_30":request.form['under_30']
    }
    Recipe.update(recipe_data)
    return redirect('/recipes')


@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    user=User.get_by_id(data)
    return render_template("display_recipe.html", recipe = Recipe.get_with_likes(id), user = user)

@app.route('/unlike/<int:id>')
def unlike(id):
    data = {
        "recipe_id": id,
        "user_id": session['user_id']
    }
    Recipe.deselect_like(data)
    return redirect('/recipes')


@app.route('/like/<int:id>')
def like(id):
    data = {
        "recipe_id": id,
        "user_id": session['user_id']
    }
    Recipe.insert_like(data)
    return redirect('/recipes')

@app.route ('/delete_recipe/<int:id>')
def delete_recipe(id):
    data = {
        'id': id
    }
    Recipe.delete_recipe(data)
    return redirect('/recipes')
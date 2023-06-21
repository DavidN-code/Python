from flask_app import app, DATABASE
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

# show all the recipes

@app.route('/recipes')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_recipes = Recipe.get_all()
    # print(all_recipes[0].user.first_name)
    return render_template('recipes.html', logged_user=logged_user, all_recipes = all_recipes)

# show the add recipe form

@app.route('/recipes/new')
def add_recipe_form():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('recipes_new.html')

# add recipe route

@app.route('/recipe/add', methods=['POST'])
def add_recipe():
    print('00000000000000000000000')
    print(request.form)
    if not Recipe.validator(request.form):
        return redirect('/recipes/new')
    print('\n')
    print('\n')
    print('\n')
    print('here')
    print(request.form)
    Recipe.save({**request.form, 'user_id':session['user_id']})
    return redirect(f'/recipes')

# view one recipe

@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    data={
        'id': recipe_id
    }
    user_data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    one_recipe = Recipe.get_by_id(data)
    print('\n'*4)
    print(one_recipe)
    return render_template('view_recipe.html', recipe_info = one_recipe, logged_user=logged_user)

# delete recipe

@app.route('/recipes/<int:recipe_id>/delete')
def delete(recipe_id):
    data={'id':recipe_id}
    print('oooooo')
    print(data)
    Recipe.delete(data)
    return redirect('/recipes')

# show edit recipe form

@app.route('/recipes/edit/<int:recipe_id>')
def editform(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : recipe_id
    }
    # User.update(data)
    one_recipe = Recipe.get_by_id(data)
    print('00000000000000')
    print(recipe_id)
    print(one_recipe.description)
    return render_template('edit_recipe.html',one_recipe=one_recipe)

# actually update the recipe

@app.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update(recipe_id):
    data = {
        # "first_name": request.form["first_name"],
        # "last_name" : request.form["last_name"],
        # "email" : request.form["email"],
        # "id" : user_id
        **request.form,
        'id' : recipe_id
    }
    if not Recipe.validator(request.form):
        return redirect(f'/recipes/edit/{recipe_id}')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>ooooooooo',data)
    Recipe.update(data)
    return redirect('/recipes')
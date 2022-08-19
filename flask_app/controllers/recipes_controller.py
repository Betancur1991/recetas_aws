from flask import render_template, redirect, request, flash, session 
from flask_app import app
from ..models.recipes import Recipe
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')

    formulario={
        'id': session['user_id']
    }

    user= User.get_by_id(formulario)
    return render_template('new_recipe.html',user=user)

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')

    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')

    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def cedit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario={
        'id': session['user_id']
    }
    
    user=User.get_by_id(formulario)
    
    formulario_receta={
        'id': id
    }
    recipe=Recipe.get_por_id(formulario_receta)

    return render_template('/edit_recipe.html',user=user, recipe=recipe)

@app.route('/update/recipe', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/')

    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id'])

    Recipe.update(request.form)
    return redirect('/dashboard')

@app.route('/show/recipe/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/')
    
    formulario={
        'id': session['user_id']
    }
    
    user=User.get_by_id(formulario)

    formulario_receta={
        'id': id
    }
    recipe=Recipe.get_por_id(formulario_receta)

    return render_template('show_recipe.html', user=user,recipe=recipe)

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    
    formulario={
        "id": id
    }
    Recipe.delete(formulario)

    return redirect('/dashboard')
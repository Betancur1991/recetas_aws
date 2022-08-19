from flask import render_template, redirect, request, flash, session, jsonify
from flask_app import app
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrate', methods=['POST'])
def registrate():
    if not User.valida_usuario(request.form):
        return redirect('/')
    else:
        pwd = bcrypt.generate_password_hash(request.form['password'])

        formulario = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": pwd
        }

        id =User.save(formulario)
        session['user_id'] =id
        
        return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    formulario={
        'id': session['user_id']
    }

    user= User.get_by_id(formulario)
    recipes=Recipe.get_all()

    return render_template('dashboard.html', user=user,recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    user=User.get_by_email(request.form)
    if not user:
        #flash('email no encontrado', 'login')
        #return redirect('/')
        return jsonify(message="Email no encontrado")

    if not bcrypt.check_password_hash(user.password,request.form['password']):
        #flash('Password incorrecto', 'login')
        #return redirect('/')
        return jsonify(message="Password incorrecto")

    session['user_id'] = user.id

    #return redirect('/dashboard')
    return jsonify(message="correcto")



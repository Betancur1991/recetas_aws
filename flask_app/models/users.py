from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX =re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:

    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def save(cls,data):
        query="Insert into users (first_name,last_name,email,password) Values (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        result=connectToMySQL('recetas').query_db(query,data)
        return result

    @staticmethod
    def valida_usuario(formulario):
        es_valido=True

        if len(formulario['first_name'])<3:
            flash('El Nombre debe de tener al menos 3 caracteres', 'registro')
            es_valido=False
        
        if len(formulario['last_name'])<3:
            flash('Apellido debe de tener al menos 3 caracteres', 'registro')
            es_valido=False

        if not EMAIL_REGEX.match(formulario['email']):
            flash('E-mail invalido', 'registro')
            es_valido=False
        
        if len(formulario['password'])<6:
            flash('Contraseña debe de tener al menos 6 caracteres', 'registro')
            es_valido=False

        if (formulario['password'].lower()) != (formulario['password']):
            es_valido=True
        else:
            flash('Contraseña debe de tener al menos una Mayúscula', 'registro')
            es_valido=False

        if re.search('[0-9]',formulario['password']):
            b="muy bien"
        else:
            flash('Contraseña debe de tener al menos un Número', 'registro')
            es_valido=False
        
        
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseña debe de coincidir con la confirmacion del password', 'registro')
            es_valido=False
        
        query =" SELECT * From users where email = %(email)s"
        result = connectToMySQL('recetas').query_db(query,formulario)
        if len(result) >= 1:
            flash('El Correo que tratas de ingresar ya se encuentra registrado', 'registro')
            es_valido=False

        return es_valido

    @classmethod
    def get_by_email(cls,data):
        query="select * from users where email= %(email)s"
        result= connectToMySQL('recetas').query_db(query,data)
        if len(result) <1:
            return False
        else:
            user = cls(result[0])
            return user

    @classmethod
    def get_by_id(cls,formulario):
        query="select * from users where id = %(id)s"
        result= connectToMySQL('recetas').query_db(query,formulario)
        user = cls(result[0])
        return user
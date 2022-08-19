from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        #LEFT JOIN
        self.first_name = data['first_name']


    @staticmethod
    def valida_receta(formulario):
        es_valido=True
        if len(formulario['name'])<3:
            flash('El Nombre debe de tener al menos 3 caracteres', 'receta')
            es_valido=False

        if len(formulario['description'])<3:
            flash('La descripcion de la receta debe de tener al menos 3 caracteres', 'receta')
            es_valido=False

        if len(formulario['instructions'])<3:
            flash('Las instrucciones de la receta debe de tener al menos 3 caracteres', 'receta')
            es_valido=False
        
        if formulario['date_made']=="":
            flash(('ingrese fecha', 'receta'))
            es_valido=False

        return es_valido

    @classmethod
    def save(cls,formulario):
        query ="Insert into recetas (name, description,instructions, date_made, under30, user_id) values(%(name)s, %(description)s,%(instructions)s, %(date_made)s, %(under30)s, %(user_id)s) "
        result= connectToMySQL('recetas').query_db(query,formulario)
        return result 

    @classmethod
    def get_all(cls):
        query ="select  recetas.*, first_name from recetas left join users on users.id=recetas.user_id; "
        results= connectToMySQL('recetas').query_db(query)
        recipes=[]
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_por_id(cls,formulario):
        query ="select  recetas.*, first_name from recetas left join users on users.id=recetas.user_id where recetas.id=%(id)s; "
        results= connectToMySQL('recetas').query_db(query,formulario)
        recipe=cls(results[0])
        return recipe
    
    @classmethod
    def update(cls,formulario):
        query ="UPDATE  recetas set name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under30=%(under30)s where id=%(id)s "
        results= connectToMySQL('recetas').query_db(query,formulario)
        return results

    @classmethod
    def delete(cls,formulario):
        query= "Delete from recetas where id= %(id)s"
        result= connectToMySQL('recetas').query_db(query,formulario)
        return result

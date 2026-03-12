from flask import Flask, render_template, request, redirect
from models import db
from models import Favorite 
import requests
import os   
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "app.db")

app = Flask (__name__)


API_URL = "https://rickandmortyapi.com/api/character"

app.config["SQLALCHEMY_DATABASE_URI"] = F"sqlsite:///{DB_PATH}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():

    #Buscar en la URL, el nro de pagina con un metodo get
    page = request.args.get("page", 1)
    name = request.args.get("name")
    
    #si hay busqueda no paginamos xd
    if name: 
        response = requests.get(API_URL, params={"name": name})
        # 200 dice que ta to bien
        if response.status_code != 200:
            return render_template("index.html", character=[], search = True, error_message = "personaje no encontrado....")
        data = response.json()
        return render_template("index.html", characters= data ["results"], search = True)
        

    # esto es nuestro listado normal con las paginas.
        response = requests.get(API_URL, params={"page": page})
    data = response.json()

    return render_template("index.html", characters=data["results"], info=data["info"],page= int(page), search= False)
    

@app.route("/save", methods = ["POST"])
def save():
    #aqui estamos guardando los campor que queremos agarrar en el front 
    api_id= request.form["api_id"]
    name = request.form["api_id"] 
    image = request.form["image"]
    page = request.form["page"]
    #si no tenemos a ese personaje en favoritos lo insertamos

    if not Favorite.query.filter_by(api_id= api_id).first():
        fav = Favorite(api_id= api_id, name = name, image= image)

        db.session.add(fav)
        db.session.commit()

    return redirect(f"/?page= {page}")


@app.route("/favorites")
def favorites():
    favorites = Favorite.query.all()

    return render_template("favorites.html", favorites = favorites)


@app.route("/delete/int:id", methods = ["POST"])
def delete (id):
    fav= Favorite.query.get(id)
    if fav:
        db.session.delete(fav)
        db.session.commit()
        
    return redirect("/favorites")

if __name__ == "__main__":
    app.run(debug=True)
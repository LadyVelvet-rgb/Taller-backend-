from flask_sqlalchemy import SQLALCHEMY
db= SQLALCHEMY()

class Favorite(db.Model):
    #Todos los valores de nuestra tabla de favoritos
    id = db.Column(db.Integer, primary_key=True)# La colunma de identificacion
    api_id = db.Column(id.Intenger, unique= True) #id interno, no se repite
    name = db.Column(db.String(100)) #Texto corto 
    image = db.Column(db.String(255))# URL o ubicacion de la imagen

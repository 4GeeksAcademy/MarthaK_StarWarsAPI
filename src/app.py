"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Characters, Starships, Favorites_characters, Favorites_planet, Favorites_starships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    # SELECT * FROM User where ID =1
    user = User.query.all()
    all_user=list(map(lambda x :x.serialize(),user))
    return jsonify (all_user)

@app.route('/planet', methods=['GET'])
def get_planet():
    # SELECT * FROM User where ID =1
    user = Planet.query.all()
    all_user=list(map(lambda x :x.serialize(),user))
    return jsonify (all_user)

@app.route('/characters', methods=['GET'])
def get_characters():
    # SELECT * FROM User where ID =1
    user = Characters.query.all()
    all_user=list(map(lambda x :x.serialize(),user))
    return jsonify (all_user)

@app.route('/starships', methods=['GET'])
def get_Starships():
    # SELECT * FROM User where ID =1
    user = Starships.query.all()
    all_user=list(map(lambda x :x.serialize(),user))
    return jsonify (all_user)

@app.route('/planet/<int:id>', methods=['GET'])
def get_one_planet(id):
    # SELECT * FROM User where ID =1
    planet=Planet.query.get(id)
    serialized=planet.serialize()
    return jsonify(serialized)

@app.route('/starships/<int:id>', methods=['GET'])
def get_one_starships(id):
    # SELECT * FROM User where ID =1
    starships=Starships.query.get(id)
    serialized=starships.serialize()
    return jsonify(serialized)

@app.route('/characters/<int:id>', methods=['GET'])
def get_one_characters(id):
    # SELECT * FROM User where ID =1
    characters=Characters.query.get(id)
    serialized=characters.serialize()
    return jsonify(serialized)


from flask import request

@app.route('/favorites_planets/filter', methods=['GET'])
def filter_favorites_planet():
    user_id = request.args.get('user_id')  
    # Realiza una consulta para obtener los favoritos de planetas del usuario
    favorites = Favorites_planet.query.filter_by(user_id=user_id).all()
    serialized = [favorite.serialize() for favorite in favorites]
    return jsonify(serialized)

@app.route('/favorites_characters/filter', methods=['GET'])
def filter_favorites_characters():
    user_id = request.args.get('user_id')  
    # Realiza una consulta para obtener los favoritos de personajes del usuario
    favorites = Favorites_characters.query.filter_by(user_id=user_id).all()
    serialized = [favorite.serialize() for favorite in favorites]
    return jsonify(serialized)

@app.route('/favorites_starships/filter', methods=['GET'])
def filter_favorites_starships():
    user_id = request.args.get('user_id')  
    # Realiza una consulta para obtener los favoritos de naves estelares del usuario
    favorites = Favorites_starships.query.filter_by(user_id=user_id).all()
    serialized = [favorite.serialize() for favorite in favorites]
    return jsonify(serialized)
 


@app.route('/planet', methods=['POST'])
def create_planet():
    body=request.json
    new_planet = Planet(name=body["name"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify ({'message':'Planet successfully created', 'planet': new_planet.serialize()})


@app.route('/characters', methods=['POST'])
def create_character():
    body=request.json
    new_characters= Characters(name=body ['name'])
    db.session.add(new_characters)
    db.session.commit()    
    return jsonify ({'message':'Characters successfully created', 'characters': new_characters.serialize()})

@app.route('/starships', methods=['POST'])
def create_starships():
    body=request.json
    new_starships= Starships(name=body['name'])
    db.session.add(new_starships)
    db.session.commit()    
    print(new_starships)
    return jsonify ({'message':'Starships successfully created', 'starships': new_starships.serialize()})


@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'You must send information in the body'}), 400
    if 'name' not in body:
        return jsonify({'msg':'The name field is required'}), 400
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify ({'msg': 'Planet with id {} does not exist'.format(planet.id)})
    planet.name=(body['name'])
    db.session.commit()
    return jsonify ({'msg': 'ok'}), 200

@app.route('/characters/<int:characters_id>', methods=['PUT'])
def update_characters(characters_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'You must send information in the body'}), 400
    if 'name' not in body:
        return jsonify({'msg':'The name field is required'}), 400
    characters = Characters.query.get(characters_id)
    if characters is None:
        return jsonify ({'msg': 'Starships with id {} does not exist'.format(Characters.id)})
    characters.name=(body['name'])
    db.session.commit()
    return jsonify ({'msg': 'ok'}), 200

@app.route('/starships/<int:starships_id>', methods=['PUT'])
def update_starships(starships_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'You must send information in the body'}), 400
    if 'name' not in body:
        return jsonify({'msg':'The name field is required'}), 400
    starships = Starships.query.get(starships_id)
    if starships is None:
        return jsonify ({'msg': 'Starships with id {} does not exist'.format(starships.id)})
    starships.name=(body['name'])
    db.session.commit()
    return jsonify ({'msg': 'ok'}), 200


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'The user with id {} does not exist'. format(user_id)}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify ({'msg': 'Deleted user'}), 200


@app.route('/starships/<int:starships_id>', methods=['DELETE'])
def delete_starships(starships_id):
    starships = Starships.query.get(starships_id)
    if starships is None:
        return jsonify({'msg': 'The Starships with id {} does not exist'. format(starships_id)}), 400
    db.session.delete(starships)
    db.session.commit()
    return jsonify ({'msg': 'Deleted Starships'}), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'The Planet with id {} does not exist'. format(planet_id)}), 400
    db.session.delete(planet)
    db.session.commit()
    return jsonify ({'msg': 'Deleted Planet'}), 200

@app.route('/characters/<int:characters_id>', methods=['DELETE'])
def delete_characters(characters_id):
    characters = Characters.query.get(characters_id)
    if characters is None:
        return jsonify({'msg': 'The Characters with id {} does not exist'. format(characters_id)}), 400
    db.session.delete(characters)
    db.session.commit()
    return jsonify ({'msg': 'Deleted Characters'}), 200
           


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

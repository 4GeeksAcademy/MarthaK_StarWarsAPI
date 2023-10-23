from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return 'Usuario de id {} con password {}' .format(self.id, self.username, self.email, self.password, self.is_active)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "active": self.is_active
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)

    def __repr__(self):
        return 'Planeta con nombre {} y id {}' .format(self.name, self.id, self.diameter, self.rotation_period, self.orbital_period)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,

        }


class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    birth_year = db.Column(db.String(50))

    def __repr__(self):
        return 'Personaje con nombre {} y id {}' .format(self.id, self.name, self.height, self.mass, self.birth_year)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "birth_year": self.birth_year,

        }


class Starships(db.Model):
    __tablename__ = 'starships'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    starship_class = db.Column(db.String(100))
    model = db.Column(db.String(100))
    length = db.Column(db.Integer)

    def __repr__(self):
        return 'Vehículo con nombre {} y id {}' .format(self.id, self.name, self.starship_class, self.model, self.length)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "starship_class": self.starship_class,
            "model": self.model,
            "length": self.length,

        }


class Favorites_characters(db.Model):
    __tablename__ = 'favorites_characters'
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    characters_id = db.Column(db.Integer, db.ForeignKey(Characters.id))
    user = relationship(User)
    characters = relationship(Characters)

    def __repr__(self):
        return 'Personaje favorito con nombre {} y id {}' .format(self.favorite_id, self.user_id, self.characters_id)

    def serialize(self):
        return {
            "favorite_id ": self.favorite_id,
            "user_id": self.user_id,
            "characters_id": self.characters_id,

        }


class Favorites_planet(db.Model):
    __tablename__ = 'favorites_planets'
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    planets_id = db.Column(db.Integer, db.ForeignKey(Planet.id))
    user = relationship(User)
    planet = relationship(Planet)

    def __repr__(self):
        return 'Planeta favorito con nombre {} y id {}' .format(self.favorite_id, self.user_id, self.planet_id)

    def serialize(self):
        return {
            "favorite_id ": self.favorite_id,
            "user_id": self.user_id,
            "planet_id": self.planets_id,

        }


class Favorites_starships(db.Model):
    __tablename__ = 'favorites_starships'
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    starships_id = db.Column(db.Integer, db.ForeignKey(Starships.id))
    user = relationship(User)
    starships = relationship(Starships)

    def __repr__(self):
        return 'Vehículo favorito con nombre {} y id {}' .format(self.favorite_id, self.user_id, self.starships_id)

    def serialize(self):
        return {
            "favorite_id ": self.favorite_id,
            "user_id": self.user_id,
            "starships.id": self.starships.id,

        }

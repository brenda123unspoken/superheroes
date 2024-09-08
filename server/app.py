#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)



api = Api(app)

# Routes
class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        return jsonify([hero.to_dict(only=('id', 'name', 'super_name')) for hero in heroes])

class HeroDetail(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if hero:
            return hero.to_dict(only=('id', 'name', 'super_name', 'hero_powers')), 200
        return {"error": "Hero not found"}, 404

class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

class PowerDetail(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if power:
            return power.to_dict(), 200
        return {"error": "Power not found"}, 404

    def patch(self, id):
        power = Power.query.get(id)
        if power:
            data = request.get_json()
            if "description" in data and len(data["description"]) >= 20:
                power.description = data["description"]
                db.session.commit()
                return power.to_dict(), 200
            return {"errors": ["Validation error: Description must be at least 20 characters long"]}, 400
        return {"error": "Power not found"}, 404

class HeroPowerCreate(Resource):
    def post(self):
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        # Validate strength
        if strength not in ['Strong', 'Weak', 'Average']:
            return {"errors": ["Invalid strength value"]}, 400

        # Validate hero and power existence
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)
        if not hero or not power:
            return {"errors": ["Hero or Power not found"]}, 404

        hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
        db.session.add(hero_power)
        db.session.commit()

        return hero_power.to_dict(), 201

# Register the API resource routes
api.add_resource(Heroes, '/heroes')
api.add_resource(HeroDetail, '/heroes/<int:id>')
api.add_resource(Powers, '/powers')
api.add_resource(PowerDetail, '/powers/<int:id>')
api.add_resource(HeroPowerCreate, '/hero_powers')

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

  

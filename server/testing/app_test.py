# from faker import Faker
# from app import app
# from models import db, Hero, Power, HeroPower


# class TestApp:
#     '''Flask application in app.py'''
    
    

#     def test_gets_heroes(self):
#         '''retrieves heroes with GET requests to /heroes.'''

#         with app.app_context():
#             fake = Faker()
#             hero1 = Hero(name=fake.name(), super_name=fake.name())
#             hero2 = Hero(name=fake.name(), super_name=fake.name())
#             db.session.add_all([hero1, hero2])
#             db.session.commit()

#             response = app.test_client().get('/heroes')
#             heroes = Hero.query.all()

#             assert response.status_code == 200
#             assert response.content_type == 'application/json'
    

#             assert [hero['id']
#                     for hero in response] == [hero.id for hero in heroes]
#             assert [hero['name']
#                     for hero in response] == [hero.name for hero in heroes]
#             assert [hero['super_name'] for hero in response] == [
#                 hero.super_name for hero in heroes]
#             for hero in response:
#                 assert 'hero_powers' not in hero

#     def test_gets_hero_by_id(self):
#         '''retrieves one hero using its ID with GET request to /heroes/<int:id>.'''

#         with app.app_context():
#             fake = Faker()
#             hero = Hero(name=fake.name(), super_name=fake.name())
#             db.session.add(hero)
#             db.session.commit()

#             response = app.test_client().get(f'/heroes/{hero.id}')

#             assert response.status_code == 200
#             assert response.content_type == 'application/json'
#             response = response.json

#             assert response['id'] == hero.id
#             assert response['name'] == hero.name
#             assert response['super_name'] == hero.super_name
#             assert 'hero_powers' in response

#     def test_returns_404_if_no_hero_to_get(self):
#         '''returns an error message and 404 status code with GET request to /heros/<int:id> by a non-existent ID.'''

#         with app.app_context():
#             response = app.test_client().get('/heroes/0')
#             assert response.status_code == 404
#             assert response.content_type == 'application/json'
#             assert response.json.get('error')
#             assert response.status_code == 404

#     def test_gets_powers(self):
#         '''retrieves powers with GET requests to /powers.'''

#         with app.app_context():
#             fake = Faker()
#             power1 = Power(name=fake.name(),
#                            description=fake.sentence(nb_words=10))
#             power2 = Power(name=fake.name(),
#                            description=fake.sentence(nb_words=10))

#             db.session.add(power1)
#             db.session.add(power2)
#             db.session.commit()

#             response = app.test_client().get('/powers')
#             powers = Power.query.all()

#             assert response.status_code == 200
#             assert response.content_type == 'application/json'
#             response = response.json

#             assert [power['id']
#                     for power in response] == [power.id for power in powers]
#             assert [power['name']
#                     for power in response] == [power.name for power in powers]
#             assert [power['description'] for power in response] == [
#                 power.description for power in powers]
#             for power in response:
#                 assert 'hero_powers' not in power

#     def test_gets_power_by_id(self):
#         '''retrieves one power using its ID with GET request to /powers/<int:id>.'''

#         with app.app_context():
#             fake = Faker()
#             power = Power(name=fake.name(),
#                           description=fake.sentence(nb_words=10))
#             db.session.add(power)
#             db.session.commit()

#             response = app.test_client().get(f'/powers/{power.id}')

#             assert response.status_code == 200
#             assert response.content_type == 'application/json'
#             response = response.json

#             assert response['id'] == power.id
#             assert response['name'] == power.name
#             assert response['description'] == power.description
#             assert 'hero_powers' not in response

#     def test_returns_404_if_no_power_to_get(self):
#         '''returns an error message and 404 status code with GET request to /powers/<int:id> by a non-existent ID.'''

#         with app.app_context():
#             response = app.test_client().get('/powers/0')
#             assert response.status_code == 404
#             assert response.content_type == 'application/json'
#             assert response.json.get('error')
#             assert response.status_code == 404

#     def test_patches_power_by_id(self):
#         '''updates one power using its ID and JSON input for its fields with a PATCH request to /powers/<int:id>.'''

#         with app.app_context():
#             fake = Faker()
#             power = Power(
#                 name=fake.name(), description=fake.sentence(nb_words=10))
#             db.session.add(power)
#             db.session.commit()

#             response = app.test_client().patch(
#                 f'/powers/{power.id}',
#                 json={
#                     'description': power.description + '(updated)'
#                 })

#             assert response.status_code == 200
#             assert response.content_type == 'application/json'
#             response = response.json

#             power_updated = Power.query.filter(Power.id == power.id).first()

#             assert response['name'] == power.name
#             assert response['description'] == power_updated.description
#             assert '(updated)' in power_updated.description

#     def test_validates_power_description(self):
#         '''returns an error message if a PATCH request to /powers/<int:id> contains a "description" value that is not a string of 20 or more characters.'''

#         with app.app_context():
#             fake = Faker()
#             power = Power(
#                 name=fake.name(), description=fake.sentence(nb_words=10))
#             db.session.add(power)
#             db.session.commit()

#             response = app.test_client().patch(
#                 f'/powers/{power.id}',
#                 json={
#                     'description': '',
#                 })

#             assert response.status_code == 400
#             assert response.content_type == 'application/json'
#             assert response.json['errors'] == ["validation errors"]

#     def test_404_no_power_to_patch(self):
#         '''returns an error message if a PATCH request to /powers/<int:id> references a non-existent power'''

#         with app.app_context():

#             response = app.test_client().patch(
#                 f'/powers/0',
#                 json={
#                     'description': '',
#                 })
#             assert response.status_code == 404
#             assert response.content_type == 'application/json'
#             assert response.json.get('error')
#             assert response.status_code == 404

#     def test_creates_hero_power(self):
#         '''creates one hero_power using a strength, a hero_id, and a power_id with a POST request to /hero_powers.'''

#         with app.app_context():

#             fake = Faker()
#             hero = Hero(name=fake.name(), super_name=fake.name())
#             power = Power(name=fake.name(),
#                           description=fake.sentence(nb_words=10))
#             db.session.add_all([hero, power])
#             db.session.commit()

#             # delete if existing in case strength differs
#             hero_power = HeroPower.query.filter_by(
#                 hero_id=hero.id, power_id=power.id).one_or_none()
#             if hero_power:
#                 db.session.delete(hero_power)
#                 db.session.commit()

#             response = app.test_client().post(
#                 'hero_powers',
#                 json={
#                     'strength': 'Weak',
#                     'hero_id': hero.id,
#                     'power_id': power.id,
#                 }
#             )

#             assert response.status_code == 201
#             assert response.content_type == 'application/json'
#             response = response.json

#             assert response['hero_id'] == hero.id
#             assert response['power_id'] == power.id
#             assert response['strength'] == 'Weak'
#             assert response['id']
#             assert response['hero']
#             assert response['power']

#             query_result = HeroPower.query.filter(
#                 HeroPower.hero_id == hero.id, HeroPower.power_id == power.id).first()
#             assert query_result.strength == 'Weak'

#     def test_validates_hero_power_strength(self):
#         '''returns an error message if a POST request to /hero_powers contains a "strength" value other than "Strong", "Weak", or "Average".'''

#         with app.app_context():
#             fake = Faker()
#             hero = Hero(name=fake.name(), super_name=fake.name())
#             power = Power(name=fake.name(),
#                           description=fake.sentence(nb_words=10))
#             db.session.add_all([hero, power])
#             db.session.commit()

#             response = app.test_client().post(
#                 'hero_powers',
#                 json={
#                     'strength': 'Cheese',
#                     'hero_id': hero.id,
#                     'power_id': power.id,
#                 }
#             )

#             assert response.status_code == 400
#             assert response.content_type == 'application/json'
#             assert response.json['errors'] == ["validation errors"]
import pytest
from faker import Faker
from app import app, db
from models import Hero, Power, HeroPower

class TestApp:
    '''Flask application in app.py'''

    @pytest.fixture
    def client(self):
        '''Fixture to create a test client and set up the database.'''
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.drop_all()

    def test_gets_heroes(self, client):
        '''retrieves heroes with GET requests to /heroes.'''
        fake = Faker()
        hero1 = Hero(name=fake.name(), super_name=fake.name())
        hero2 = Hero(name=fake.name(), super_name=fake.name())
        db.session.add_all([hero1, hero2])
        db.session.commit()

        response = client.get('/heroes')
        heroes = Hero.query.all()

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        response_json = response.json

        assert [hero['id'] for hero in response_json] == [hero.id for hero in heroes]
        assert [hero['name'] for hero in response_json] == [hero.name for hero in heroes]
        assert [hero['super_name'] for hero in response_json] == [hero.super_name for hero in heroes]
        for hero in response_json:
            assert 'hero_powers' not in hero

    def test_gets_hero_by_id(self, client):
        '''retrieves one hero using its ID with GET request to /heroes/<int:id>.'''
        fake = Faker()
        hero = Hero(name=fake.name(), super_name=fake.name())
        db.session.add(hero)
        db.session.commit()

        response = client.get(f'/heroes/{hero.id}')

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        response_json = response.json

        assert response_json['id'] == hero.id
        assert response_json['name'] == hero.name
        assert response_json['super_name'] == hero.super_name
        assert 'hero_powers' in response_json

    def test_returns_404_if_no_hero_to_get(self, client):
        '''returns an error message and 404 status code with GET request to /heroes/<int:id> by a non-existent ID.'''
        response = client.get('/heroes/0')
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        assert 'error' in response.json

    def test_gets_powers(self, client):
        '''retrieves powers with GET requests to /powers.'''
        fake = Faker()
        power1 = Power(name=fake.name(), description=fake.sentence(nb_words=10))
        power2 = Power(name=fake.name(), description=fake.sentence(nb_words=10))
        db.session.add_all([power1, power2])
        db.session.commit()

        response = client.get('/powers')
        powers = Power.query.all()

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        response_json = response.json

        assert [power['id'] for power in response_json] == [power.id for power in powers]
        assert [power['name'] for power in response_json] == [power.name for power in powers]
        assert [power['description'] for power in response_json] == [power.description for power in powers]
        for power in response_json:
            assert 'hero_powers' not in power

    def test_gets_power_by_id(self, client):
        '''retrieves one power using its ID with GET request to /powers/<int:id>.'''
        fake = Faker()
        power = Power(name=fake.name(), description=fake.sentence(nb_words=10))
        db.session.add(power)
        db.session.commit()

        response = client.get(f'/powers/{power.id}')

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        response_json = response.json

        assert response_json['id'] == power.id
        assert response_json['name'] == power.name
        assert response_json['description'] == power.description
        assert 'hero_powers' not in response_json

    def test_returns_404_if_no_power_to_get(self, client):
        '''returns an error message and 404 status code with GET request to /powers/<int:id> by a non-existent ID.'''
        response = client.get('/powers/0')
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        assert 'error' in response.json

    def test_patches_power_by_id(self, client):
        '''updates one power using its ID and JSON input for its fields with a PATCH request to /powers/<int:id>.'''
        fake = Faker()
        power = Power(name=fake.name(), description=fake.sentence(nb_words=10))
        db.session.add(power)
        db.session.commit()

        response = client.patch(
            f'/powers/{power.id}',
            json={'description': power.description + '(updated)'}
        )

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        response_json = response.json

        power_updated = Power.query.get(power.id)

        assert response_json['name'] == power.name
        assert response_json['description'] == power_updated.description
        assert '(updated)' in power_updated.description

    def test_validates_power_description(self, client):
        '''returns an error message if a PATCH request to /powers/<int:id> contains a "description" value that is not a string of 20 or more characters.'''
        fake = Faker()
        power = Power(name=fake.name(), description=fake.sentence(nb_words=10))
        db.session.add(power)
        db.session.commit()

        response = client.patch(
            f'/powers/{power.id}',
            json={'description': ''}
        )

        assert response.status_code == 400
        assert response.content_type == 'application/json'
        assert response.json['errors'] == ["Validation error: Description must be at least 20 characters long"]

    def test_404_no_power_to_patch(self, client):
        '''returns an error message if a PATCH request to /powers/<int:id> references a non-existent power.'''
        response = client.patch(
            '/powers/0',
            json={'description': ''}
        )
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        assert 'error' in response.json

    def test_creates_hero_power(self, client):
        '''creates one hero_power using a strength, a hero_id, and a power_id with a POST request to /hero_powers.'''
        fake = Faker()
        hero = Hero(name=fake.name(), super_name=fake.name())
        power = Power(name=fake.name(), description=fake.sentence(nb_words=10))
        db.session.add_all([hero, power])
        db.session.commit()

        response = client.post(
            '/hero_powers',
            json={
                'strength': 'Weak',
                'hero_id': hero.id,
                'power_id': power.id,
            }
        )

        assert response.status_code == 201
        assert response.content_type == 'application/json'
        response_json = response.json

        assert response_json['hero_id'] == hero.id
        assert response_json['power_id'] == power.id
        assert response_json['strength'] == 'Weak'
        assert 'id' in response_json
        assert 'hero' in response_json
        assert 'power' in response_json

        hero_power = HeroPower.query.filter_by(
            hero_id=hero.id, power_id=power.id
        ).first()
        assert hero_power.strength == 'Weak'

    def test_validates_hero_power_strength(self, client):
        '''returns an error message if a POST request to /hero_powers contains a "strength" value other than "Strong", "Weak", or "Average".'''
        fake = Faker()
        hero = Hero(name=fake.name(), super_name=fake.name())
        power = Power(name=fake.name(), description=fake.sentence(nb_words=10))
        db.session.add_all([hero, power])
        db.session.commit()

        response = client.post(
            '/hero_powers',
            json={
                'strength': 'Cheese',
                'hero_id': hero.id,
                'power_id': power.id,
            }
        )

        assert response.status_code == 400
        assert response.content_type == 'application/json'
        assert response.json['errors'] == ["Invalid strength value"]

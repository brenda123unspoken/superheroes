from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates 
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    # add relationship
    powers = db.relationship("Power", secondary="hero_powers", back_populates="heroes")
    hero_powers = db.relationship("HeroPower", back_populates="hero")
    # add serialization rules
    serialize_rules = ('-hero_powers',)
    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # add relationship
    heroes = relationship("Hero", secondary="hero_powers", back_populates="powers")
    hero_powers = relationship("HeroPower", back_populates="power")

    # add serialization rules
    serialize_rules = ('-hero_powers',)  
    # add validation
    @validates('description')
    def validate_description(self, key, value):
        if not value:
            raise ValueError("Description must be present")
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value

    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)

    # add relationships
    hero_id = db.Column(db.Integer, ForeignKey('heroes.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates="hero_powers")

    power_id = db.Column(db.Integer, ForeignKey('powers.id', ondelete="CASCADE"))
    power = relationship("Power", back_populates="hero_powers")

    # add serialization rules
    serialize_rules = ('-hero', '-power',) 
    # add validation
    @validates('strength')
    def validate_strength(self, key, value):
        allowed_values = {'Strong', 'Weak', 'Average'}
        if value not in allowed_values:
            raise ValueError(f"Strength must be one of {allowed_values}")
        return value


    def __repr__(self):
        return f'<HeroPower {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'strength': self.strength,
            'hero_id': self.hero_id,
           'power_id': self.power_id
        }

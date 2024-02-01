from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)  

    # Add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="pizza")
    # Add serialization
    serialize_rules = ("-restaurant_pizzas.pizza",)

    def __repr__(self):
        return f"<Pizza {self.id} : {self.name}, {self.ingredients}>"


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)  

    # Add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="restaurant")
    # Add serialization
    serialize_rules = ("-restaurant_pizzas.restaurant",)

    def __repr__(self):
        return f"<Restaurant {self.id} : {self.name}, {self.address}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))

    # Add relationships
    pizza = db.relationship("Pizza", back_populates="restaurant_pizzas")
    restaurant = db.relationship("Restaurant", back_populates="restaurant_pizzas")
    # Add serialization
    serialize_rules = ("-pizza.restaurant_pizzas", "-restaurant.restaurant_pizzas")

    # Add validation
    @validates("price")
    def validate_price(self, key, value):
        if value is None or value < 0:
            raise ValueError(f"{key} must have a value between 1 and 30")

        return value

    def __repr__(self):
        return f"<PizzaRe {self.id} : {self.price} : {self.pizza_id} : {self.restaurant_id}>"
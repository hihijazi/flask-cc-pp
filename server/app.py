#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def restaurants():
    restaurants = Restaurant.query.all()
    response = make_response(
        [restaurant.to_dict(rules=("-restaurant_pizzas", )) for restaurant in restaurants], 200
    )

    return response

@app.route('/restaurants/<int:id>', methods=["GET"])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()

    if restaurant is None:
        return make_response({"error": "Restaurant not found"}, 404)

    response = make_response(restaurant.to_dict(rules=("-restaurant_pizzas",)), 200)

    return response


@app.route("/pizzas", methods=["GET"])
def pizzas():
    pizzas = Pizza.query.all()
    response = make_response(
        [pizza.to_dict(rules=("-restaurant_pizzas",)) for pizza in pizzas], 200
    )

    return response


@app.route("/pizzas/<int:id>", methods=["GET"])
def pizzas_by_id(id):
    pizza = Pizza.query.filter(Pizza.id == id).first()

    if pizza is None:
        return make_response({"error": "Pizza not found"}, 404)

    response = make_response(pizza.to_dict(rules=("-restaurant_pizzas",)), 200)

    return response

@app.route("/restaurant_pizzas", methods=["POST"])
def restaurant_pizzas():
    try:
        form_data = request.get_json()

        if form_data is None or 'price' not in form_data:  # Check if 'price' exists in form_data
            return make_response({"error": "Price field is missing"}, 400)

        # Check if 'price' is between 1 and 30
        price = form_data['price']
        if not (1 <= price <= 30):
            return make_response({"error": "Price must be between 1 and 30"}, 400)

        new_restaurant_pizza = RestaurantPizza(
            price=price,
            restaurant_id=form_data.get("restaurant_id"),
            pizza_id=form_data.get("pizza_id"),
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        response = make_response(new_restaurant_pizza.to_dict(), 201)
    except Exception as e:
        response = make_response({"error": str(e)}, 500)

    return response









@app.route("/restaurant_pizzas/<int:id>", methods=["DELETE"])
def restaurant_pizzas_by_id(id):
    restaurant_pizza = RestaurantPizza.query.filter(RestaurantPizza.id == id).first()

    if restaurant_pizza is None:
        return make_response({"error": "RestaurantPizza not found"}, 404)

    db.session.delete(restaurant_pizza)
    db.session.commit()

    return make_response({}, 204)

#API Solution 


class RestaurantApi(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        response = make_response(
            [restaurant.to_dict(rules=("-restaurant_pizza",)) for restaurant in restaurants], 200
        )

        return response


api.add_resource(RestaurantApi, "/restaurants_api")


class RestaurantApiById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()

        if restaurant is None:
            return make_response({"error": "Restaurant not found"}, 404)

        response = make_response(restaurant.to_dict(), 200)

        return response



api.add_resource(RestaurantApiById, "/restaurants_api/<int:id>")




if __name__ == '__main__':
    app.run(port=5555, debug=True)

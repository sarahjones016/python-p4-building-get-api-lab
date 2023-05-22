#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():

    all_bakeries = Bakery.query.all()
    all_bakeries_serialized = [bakery.to_dict() for bakery in all_bakeries]

    response = make_response(
        jsonify(all_bakeries_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery_by_id = Bakery.query.filter(Bakery.id == id).first()

    bakery_by_id_serialized = bakery_by_id.to_dict()

    response = make_response(
        jsonify(bakery_by_id_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [baked_good.to_dict() for baked_good in baked_goods_by_price]

    response = make_response(
        jsonify(baked_goods_by_price_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    most_expensive_baked_good_serialized = most_expensive_baked_good.to_dict()

    response = make_response(
        jsonify(most_expensive_baked_good_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=555, debug=True)

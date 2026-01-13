#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
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


# GET /bakeries - returns all bakeries
@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    return make_response(jsonify([b.to_dict() for b in all_bakeries]), 200)


# GET /bakeries/<int:id> - returns a single bakery with its baked goods
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    bakery_dict = bakery.to_dict()
    bakery_dict['baked_goods'] = [bg.to_dict() for bg in bakery.baked_goods]
    return make_response(jsonify(bakery_dict), 200)


# GET /baked_goods/by_price - returns baked goods sorted by price descending
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return make_response(jsonify([bg.to_dict() for bg in baked_goods]), 200)


# GET /baked_goods/most_expensive - returns the single most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good is None:
        return make_response(jsonify({}), 200)
    return make_response(jsonify(baked_good.to_dict()), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

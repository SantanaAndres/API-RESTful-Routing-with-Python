import random
from types import NoneType
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)



# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random():
    cafe = db.session.execute(db.select(Cafe))
    all_cafes = cafe.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(
        cafe={
            "can_take_calls": random_cafe.can_take_calls,
            "coffee_price": random_cafe.coffee_price,
            "has_sockets": random_cafe.has_sockets,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi,
            "id": random_cafe.id,
            "img_url":random_cafe.img_url,
            "map_url":random_cafe.map_url,
            "name":random_cafe.name,
            "seats":random_cafe.seats
        }   
    )

@app.route("/all")
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe))
    all_cafes = cafes.scalars().all()
    cafe_list = []
    for cafe in all_cafes:
        cafe_list.append(cafe.to_dict())
    return jsonify(cafe=cafe_list)

@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404# HTTP POST - Create Record


@app.route("/add", methods=["POST"])
def add():
    cafe = Cafe(
        name=request.args.get("name"),
        map_url=request.args.get("map_url"),
        img_url=request.args.get("img_url"),
        location=request.args.get("location"),
        seats=request.args.get("seats"),
        has_toilet=request.args.get("has_toilet"),
        has_wifi=request.args.get("has_wifi"),
        has_sockets=request.args.get("has_sockets"),
        can_take_calls=request.args.get("can_take_calls"),
        coffee_price=request.args.get("coffee_price")
    )
    db.session.add(cafe)
    db.session.commit()
    return jsonify(
        response={"success": "Successfully added the new cafe."}
        )
# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update(cafe_id):    
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price=request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    api_key = request.args.get("api-key")
    if cafe:
        if api_key == "TopSecretAPIKey":
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api_key"), 403
    else: 
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database"}), 404

if __name__ == '__main__':
    app.run(debug=True)

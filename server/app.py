from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import QueuePool

from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
#from database import Report, reports_schema


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # change this IRL

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://{user}:{password}@{host}:3309/{database}".format(
    user="root", password="", host="localhost", database="python_bi_demo",
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "poolclass": QueuePool,
    "pool_size": 10,
    "pool_recycle": 300,
    "pool_use_lifo": True,
    "pool_pre_ping": True,
}

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


@app.route("/")
def hello_world():
    return "Hello World 1!"


@app.route("/reports", methods=["GET"])
def reports():
    reports = [{"report_id": 1, "report_name": "Sales"}]

    reports_list = Report.query.all()
    result = reports_schema.dump(reports_list)
    return jsonify(result.data)


@app.route("/url_variables/<string:name>/<int:age>")
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")


"""
@app.route("/planets", methods=["GET"])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result.data)


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message="That email already exists."), 409
    else:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        user = User(
            first_name=first_name, last_name=last_name, email=email, password=password
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully."), 201


@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@app.route("/planet_details/<int:planet_id>", methods=["GET"])
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result.data)
    else:
        return jsonify(message="That planet does not exist"), 404


@app.route("/add_planet", methods=["POST"])
@jwt_required
def add_planet():
    planet_name = request.form["planet_name"]
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify("There is already a planet by that name"), 409
    else:
        planet_type = request.form["planet_type"]
        home_star = request.form["home_star"]
        mass = float(request.form["mass"])
        radius = float(request.form["radius"])
        distance = float(request.form["distance"])

        new_planet = Planet(
            planet_name=planet_name,
            planet_type=planet_type,
            home_star=home_star,
            mass=mass,
            radius=radius,
            distance=distance,
        )

        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message="You added a planet"), 201


@app.route("/update_planet", methods=["PUT"])
@jwt_required
def update_planet():
    planet_id = int(request.form["planet_id"])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.form["planet_name"]
        planet.planet_type = request.form["planet_type"]
        planet.home_star = request.form["home_star"]
        planet.mass = float(request.form["mass"])
        planet.radius = float(request.form["radius"])
        planet.distance = float(request.form["distance"])
        db.session.commit()
        return jsonify(message="You updated a planet"), 202
    else:
        return jsonify(message="That planet does not exist"), 404


@app.route("/remove_planet/<int:planet_id>", methods=["DELETE"])
@jwt_required
def remove_planet(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message="You deleted a planet"), 202
    else:
        return jsonify(message="That planet does not exist"), 404
"""


# database models
class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Report(db.Model):
    __tablename__ = "report"

    report_id = Column(Integer, primary_key=True)
    report_name = Column(String)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "password")


class ReportSchema(ma.Schema):
    class Meta:
        fields = (
            "report_id",
            "report_name",
        )


user_schema = UserSchema()
users_schema = UserSchema(many=True)

report_schema = ReportSchema()
reports_schema = ReportSchema(many=True)


if __name__ == "__main__":
    app.run()

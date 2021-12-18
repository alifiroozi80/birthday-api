from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import os

app = Flask(__name__)
uri = os.environ.get("DATABASE_URL")
API_KEY = os.environ.get("API_KEY")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(uri, "sqlite:///users.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=False)
    family = db.Column(db.String(250), nullable=False, unique=True)
    birth = db.Column(db.String(100), nullable=False, unique=False)

    def __repr__(self):
        return f"<User>: {self.family}"

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Uncomment the line below first time you run the script then delete it.
# db.create_all()


@app.route("/")
def home():
    return \
        "<h1>API Documentation can be found " \
        "<a href='https://documenter.getpostman.com/view/16109796/UVRAHmsZ'>Here</a></h1>"


@app.route("/all")
def get_all():
    users = User.query.all()
    return jsonify(users=[user.to_dict() for user in users]), 200


@app.route("/search")
def search():
    family = request.args.get("family").lower().title()
    user = User.query.filter_by(family=family).first()
    if user:
        return jsonify(user=user.to_dict()), 200
    else:
        return jsonify(error={"Not Found": "Sorry, we couldn't find any match with that family."}), 404


@app.route("/add", methods=["POST"])
def add():
    api_key = request.args.get("api-key")
    if API_KEY == api_key:
        try:
            new_user = User(
                name=request.form.get("name"),
                family=request.form.get("family"),
                birth=request.form.get("birth")
            )
            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return jsonify(error={"Database Error": "This Family is already exist in Database."}), 400
        else:
            return jsonify(response={"success": "Successfully added the new user."}), 200
    else:
        return jsonify(error="Sorry, That's not allowed. Make sure you have the correct api-key."), 403


@app.route("/update/user_id=<int:user_id>", methods=["PATCH"])
def update(user_id):
    api_key = request.args.get("api-key")
    if API_KEY == api_key:
        user = User.query.get(user_id)
        if user:
            name = request.args.get("name")
            family = request.args.get("family")
            birth = request.args.get("birth")

            if name:
                user.name = name
                db.session.commit()
                return jsonify({"success": "Successfully update the name."}), 200
            if family:
                user.family = family
                db.session.commit()
                return jsonify({"success": "Successfully update the family."}), 200
            if birth:
                user.birth = birth
                db.session.commit()
                return jsonify({"success": "Successfully update the birth."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry, we couldn't find any match with that ID."}), 404
    else:
        return jsonify(error="Sorry, That's not allowed. Make sure you have the correct api-key."), 403


@app.route("/delete/user_id=<int:user_id>", methods=["DELETE"])
def delete(user_id):
    api_key = request.args.get("api-key")
    if API_KEY == api_key:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(success="Successfully deleted the user."), 200
        else:
            return jsonify(error={"Not Found": "Sorry, we couldn't find any match with that ID."}), 404
    else:
        return jsonify(error="Sorry, That's not allowed. Make sure you have the correct api-key."), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

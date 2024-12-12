from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'

# Create DB Model Base
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe Table Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        """Converts Cafe object to a dictionary."""
        # # Method 1.
        # dictionary = {}
        # # Loop through each column in the data record
        # for column in self.__table__.columns:
        #     # Create a new dictionary entry;
        #     # where the key is the name of the column
        #     # and the value is the value of the column
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary

        # Method 2. Alternatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Get a Random Cafe
@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    if not all_cafes:
        return jsonify(error={"message": "No cafes found."}), 404
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())

# HTTP GET - Get All Cafes
@app.route("/all")
def get_cafes():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    cafes = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=cafes)

# HTTP GET - Search Cafes by Location
@app.route("/search")
def find_cafe():
    location = request.args.get("loc")
    if not location:
        return jsonify(error={"message": "Location parameter is required."}), 400

    cafes = db.session.execute(db.select(Cafe).where(Cafe.location==location)).scalars().all()
    if cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])
    else:
        return jsonify(error={"message": "No cafes found at the specified location."}), 404



# HTTP POST - Add a New Cafe
@app.route("/add", methods=["POST"])
def add_cafe():
    data = request.form

    try:
        new_cafe = Cafe(
            name=data.get("name"),
            map_url=data.get("map_url"),
            img_url=data.get("img_url"),
            location=data.get("location"),
            seats=data.get("seats"),
            has_toilet=bool(data.get("has_toilet")),
            has_wifi=bool(data.get("has_wifi")),
            has_sockets=bool(data.get("has_sockets")),
            can_take_calls=bool(data.get("can_take_calls")),
            coffee_price=data.get("coffee_price")
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})
    except Exception as e:
        return jsonify(error={"message": f"Failed to add cafe: {str(e)}"}), 500



# HTTP PATCH - Update Coffee Price
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):

    new_price = request.args.get("coffee_price")
    if not new_price:
        return jsonify(error={"message": "Coffee price is required."}), 400

    try:
        cafe_to_update = db.get_or_404(Cafe, cafe_id)
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})

    except NotFound:
        return jsonify(error={"message": "Cafe not found."}), 404

    except Exception as e:
        return jsonify(error={"message": f"Failed to update price: {str(e)}"}), 500


# HTTP DELETE - Delete a Cafe
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key != "TopSecretAPIKey":
        return jsonify(error={"message": "Invalid API key."}), 403

    try:
        cafe_to_delete = db.get_or_404(Cafe, cafe_id)
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe."})

    except NotFound:
        return jsonify(error={"message": "Cafe not found."}), 404

    except Exception as e:
        return jsonify(error={"message": f"Failed to delete cafe: {str(e)}"}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

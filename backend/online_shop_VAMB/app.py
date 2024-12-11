from flask import Flask, jsonify, send_from_directory, abort, request
from models import db, User, Product, Category, Manufacturer, Model, Partmanufacturer
from werkzeug.security import check_password_hash
from flask_cors import CORS
from flask_migrate import Migrate
import os

app = Flask(__name__, static_folder='static')
migrate = Migrate(app, db)

app.debug = True

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/diplomna_v2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return "Hello, Flask with PostgreSQL!"

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

@app.route('/images/<filename>')
def uploaded_file(filename):
    directory = os.path.join(app.root_path, 'static/images')
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        return send_from_directory(directory, filename)
    else:
        abort(404)

@app.route('/api/form-options', methods=['GET'])
def get_form_options():
    try:
        car_manufacturers = Manufacturer.query.all()
        car_manufacturer_data = [{"id": m.id, "name": m.name} for m in car_manufacturers]

        categories = Category.query.all()
        category_data = [{"id": c.id, "name": c.name} for c in categories]

        product_manufacturers = Partmanufacturer.query.all()
        product_manufacturer_data = [{"id": pm.id, "name": pm.name} for pm in product_manufacturers]

        return jsonify({
            "carManufacturers": car_manufacturer_data,
            "productCategories": category_data,
            "productManufacturers": product_manufacturer_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/car-models/<manufacturer_id>', methods=['GET'])
def get_car_models(manufacturer_id):
    try:
        models = Model.query.filter_by(manufacturer_id=manufacturer_id).all()
        model_data = [{"id": m.id, "name": m.name} for m in models]
        return jsonify(model_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search-products', methods=['POST'])
def search_products():
    data = request.json
    car_manufacturer = data.get('manufacturer')
    car_model = data.get('model')
    product_category = data.get('category')
    serial_number = data.get('serial_num')
    product_manufacturer = data.get('product_manufacturer')

    query = Product.query

    if car_manufacturer:
        query = query.filter(Product.car_manufacturer == car_manufacturer)
    if car_model:
        query = query.filter(Product.car_model == car_model)
    if product_category:
        query = query.filter(Product.category == product_category)
    if serial_number:
        query = query.filter(Product.serial_num == serial_number)
    if product_manufacturer:
        query = query.filter(Product.manufacturer == product_manufacturer)

    results = query.all()

    return jsonify([product.serialize() for product in results])

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "message": "Моля, попълнете всички полета."}), 400

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        token = "example-token"
        return jsonify({"success": True, "token": token}), 200
    else:
        return jsonify({"success": False, "message": "Невалиден имейл или парола."}), 401


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

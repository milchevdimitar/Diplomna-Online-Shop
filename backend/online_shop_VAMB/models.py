from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=1)
)

product_image = db.Table('product_image',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'), primary_key=True)
)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path_to_image = db.Column(db.String(255), nullable=False)

    products = db.relationship('Product', secondary=product_image, back_populates='images')

    def __repr__(self):
        return f'<Image ID: {self.id}, Path: {self.path_to_image}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rank = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}, Rank: {self.rank}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    manufacturer = db.Column(db.String(120), nullable=False)
    price_bgn = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    serial_num = db.Column(db.String(120), unique=True, nullable=False)
    curr_available = db.Column(db.Integer, default=0)

    orders = db.relationship('Order', secondary=order_product, back_populates='products')
    images = db.relationship('Image', secondary=product_image, back_populates='products')
    models = db.relationship('Model', secondary='product_model', back_populates='products')

    def __repr__(self):
        return f'<Product {self.name}, Available: {self.curr_available}>'

    def serialize(self):
        
        if (self.curr_available > 0):
            curr_avail_str = "В наличност"
        else:
            curr_avail_str = "Не е налично"

        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'manufacturer': self.manufacturer,
            'price_bgn': self.price_bgn,
            'description': self.description,
            'serial_num': self.serial_num,
            'curr_available': curr_avail_str,
            'images': [f'http://localhost:5000/images/{image.path_to_image}' for image in self.images],
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    payment_type = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default="pending")
    curr_state = db.Column(db.String(50), nullable=False, default="processing")

    user = db.relationship('User', backref=db.backref('orders', lazy=True))

    products = db.relationship('Product', secondary=order_product, back_populates='orders')

    def __repr__(self):
        return f'<Order {self.id}, State: {self.curr_state}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'<Manufacturer {self.name}>'

class Partmanufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'<Partmanufacturer {self.name}>'

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)
    manufacturer = db.relationship('Manufacturer', backref=db.backref('models', lazy=True))
    products = db.relationship('Product', secondary='product_model', back_populates='models')

    def __repr__(self):
        return f'<Model ID: {self.id}, Manufacturer: {self.manufacturer.name}>'

product_model = db.Table('product_model',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True)
)

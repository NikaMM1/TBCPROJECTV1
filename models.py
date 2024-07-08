from ext import db
from flask_login import UserMixin

def register_user(username, password):
    new_user = User(username=username, password=password)  
    db.session.add(new_user)
    db.session.commit()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=True)

    orders = db.relationship('Order', backref='user')

class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image_url = db.Column(db.String(256))

class Order(db.Model):
    __tablename__ = 'orders'  

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    card_number = db.Column(db.String(16))
    card_name = db.Column(db.String(100))
    cvv = db.Column(db.String(4))
    food_item = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    order_items = db.relationship('OrderItem', backref='order', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'  
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    name = db.Column(db.String(128))
    description = db.Column(db.String(256))
    price = db.Column(db.Float)
    


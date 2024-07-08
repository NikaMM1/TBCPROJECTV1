
from ext import app, db
from models import MenuItem

with app.app_context():
    db.create_all()  
    
    menu_items = [
        MenuItem(name='Pizza', description='Delicious pizza with cheese and toppings', price=12.99, image_url='pizza.jpg'),
        MenuItem(name='Burger', description='Juicy burger with fries', price=8.99, image_url='burger.jpg'),
        MenuItem(name='Salad', description='Fresh garden salad', price=7.99, image_url='salad.jpg'),
        MenuItem(name='Pasta', description='Spaghetti with marinara sauce', price=10.99, image_url='pasta.jpg'),
        MenuItem(name='Sandwich', description='Classic ham and cheese sandwich', price=6.99, image_url='sandwich.jpg'),
    ]

    db.session.bulk_save_objects(menu_items)
    db.session.commit()

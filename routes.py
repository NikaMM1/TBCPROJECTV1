from flask import render_template, redirect, url_for, flash, session, current_app, request
from flask_login import login_user, logout_user, login_required, current_user
from ext import app, db, login_manager
from models import User, Order, MenuItem, OrderItem, register_user
from forms import RegisterForm, LoginForm, OrderForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    menu_items = MenuItem.query.all()
    return render_template('menu.html', menu_items=menu_items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists', 400
        register_user(username, password)
        return 'User registered successfully', 201
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    form = OrderForm()

    current_app.logger.info(f"Request method: {request.method}")
    if request.method == 'POST':
        current_app.logger.info(f"Form data: {request.form}")

    if form.validate_on_submit():
        try:
            new_order = Order(
                email=form.email.data,
                address=form.address.data,
                card_number=form.card_number.data,
                card_name=form.card_name.data,
                cvv=form.cvv.data,
                food_item=form.food_item.data,
                user_id=current_user.id
            )
            db.session.add(new_order)
            db.session.flush() 

            current_app.logger.info(f"New order created with ID: {new_order.id}")

            cart_items = session.get('cart', [])
            current_app.logger.info(f"Cart items: {cart_items}")
            for item in cart_items:
                order_item = OrderItem(
                    order_id=new_order.id, 
                    name=item['name'],
                    description=item['description'],
                    price=item['price']
                )
                db.session.add(order_item)
                current_app.logger.info(f"Order item added: {order_item}")

            db.session.commit()
            session.pop('cart', None)
            flash('Order placed successfully.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            current_app.logger.error(f"Error: {e}")
            flash('An error occurred while placing the order.', 'danger')
            db.session.rollback()
    

    cart_items = session.get('cart', [])
    current_app.logger.info(f"Cart items on form load: {cart_items}")

    return render_template('order.html', form=form, cart_items=cart_items)

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('index'))
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/orders/delete/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('index'))
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        flash('Order deleted successfully.')
    return redirect(url_for('admin_orders'))

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    item = MenuItem.query.get(item_id)
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('menu'))

    if 'cart' not in session:
        session['cart'] = []
    
    for cart_item in session['cart']:
        if cart_item.get('item_id') == item.id:
            flash(f"{item.name} is already in the cart.", 'info')
            return redirect(url_for('menu'))
    
    session['cart'].append({
        'item_id': item.id, 
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'image_url': item.image_url
    })
    
    session.modified = True
    current_app.logger.info(f"Item added to cart: {session['cart'][-1]}")
    flash(f"{item.name} added to cart successfully.", 'success')
    return redirect(url_for('menu'))

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    new_cart = [item for item in cart if item.get('item_id') != item_id]
    
    if len(new_cart) == len(cart):
        flash('Item not found in the cart.', 'error')
    else:
        session['cart'] = new_cart
        session.modified = True
        flash('Item removed from cart successfully.', 'success')
    
    return redirect(url_for('order'))

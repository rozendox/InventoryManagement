from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.inventory import bp
from app.models import Order, Item, Location, OrderItem
from app import db
from datetime import datetime

@bp.route('/orders')
@login_required
def orders():
    orders = Order.query.all()
    return render_template('inventory/orders.html', orders=orders)

@bp.route('/orders/new', methods=['GET', 'POST'])
@login_required
def new_order():
    if request.method == 'POST':
        location_id = request.form.get('location_id')
        items = request.form.getlist('items[]')
        quantities = request.form.getlist('quantities[]')
        note = request.form.get('note')
        
        # Generate order number (timestamp-based)
        order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        order = Order(
            order_number=order_number,
            requester_id=current_user.id,
            location_id=location_id,
            note=note
        )
        db.session.add(order)
        
        for item_id, qty in zip(items, quantities):
            order_item = OrderItem(
                order=order,
                item_id=int(item_id),
                quantity=int(qty)
            )
            db.session.add(order_item)
        
        db.session.commit()
        flash('Order created successfully', 'success')
        return redirect(url_for('inventory.orders'))
    
    items = Item.query.all()
    locations = Location.query.all()
    return render_template('inventory/new_order.html', items=items, locations=locations)

@bp.route('/delivered')
@login_required
def delivered():
    delivered_orders = Order.query.filter_by(status='delivered').all()
    return render_template('inventory/delivered.html', orders=delivered_orders)

@bp.route('/items')
@login_required
def items():
    items = Item.query.all()
    return render_template('inventory/items.html', items=items)

@bp.route('/items/add', methods=['POST'])
@login_required
def add_item():
    name = request.form.get('name')
    description = request.form.get('description')
    quantity = request.form.get('quantity', type=int)
    
    item = Item(name=name, description=description, quantity=quantity)
    db.session.add(item)
    db.session.commit()
    
    flash('Item added successfully', 'success')
    return redirect(url_for('inventory.items'))

@bp.route('/orders/<int:order_id>/deliver', methods=['POST'])
@login_required
def deliver_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'delivered'
    db.session.commit()
    flash('Order marked as delivered', 'success')
    return redirect(url_for('inventory.orders'))
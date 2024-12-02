from flask import render_template
from flask_login import login_required
from app.main import bp
from app.models import Order, Item
from datetime import datetime, date


@bp.route('/')
@login_required
def index():
    pending_orders = Order.query.filter_by(status='pending').all()
    delivered_today = Order.query.filter_by(
        status='delivered'
    ).filter(
        Order.created_at >= date.today()
    ).all()
    total_items = Item.query.count()

    return render_template('main/index.html',
                           pending_orders=pending_orders,
                           delivered_today=delivered_today,
                           total_items=total_items)

from app import create_app, db
from app.models import User, Location


def init_db():
    app = create_app()
    with app.app_context():

        db.create_all()

        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True,
                is_warehouse_staff=True
            )
            admin.set_password('admin123')
            db.session.add(admin)

        locations = [
            ('point A', 'Main Warehouse'),
            ('Office Building', 'Principal Office Building'),
            ('Work Station', ' Main Workstation')
        ]

        for name, description in locations:
            if not Location.query.filter_by(name=name).first():
                location = Location(name=name, description=description)
                db.session.add(location)

        db.session.commit()
        print("Database initialized successfully!")


if __name__ == '__main__':
    init_db()

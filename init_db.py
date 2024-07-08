from ext import db, app
import models

with app.app_context():
    db.create_all()
    print("Database tables created")

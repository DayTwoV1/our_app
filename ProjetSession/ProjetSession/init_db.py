from monapp import db
from monapp import app

with app.app_context():
    db.create_all()
    print("Base de données créée.")

from app import create_app
from app.utils.database import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # This will create all tables if they don't exist
        db.create_all()
    app.run(debug=True)

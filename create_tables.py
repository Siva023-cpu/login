from app import db, app, User  # adjust if User isn't directly importable

with app.app_context():
    db.create_all()
    print("✅ Tables created.")

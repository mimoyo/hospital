from app import app
from models import db, Category

with app.app_context():
    db.session.add_all([
        Category(name="Высшая"),
        Category(name="Первая"),
        Category(name="Вторая"),
        Category(name="Без категории")
    ])
    db.session.commit()
    print("Категории врачей добавлены")

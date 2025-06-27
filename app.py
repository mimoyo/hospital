from flask import Flask
from models import db
from modules import register_blueprints

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'  # нужен для flash()

db.init_app(app)

# Создание таблиц
with app.app_context():
    db.create_all()

register_blueprints(app)

# ========== Запуск сервера ==========
if __name__ == '__main__':
    app.run(debug=True)

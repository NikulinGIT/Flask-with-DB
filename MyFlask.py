from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# Создание экземпляра Flask
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
# Настройка подключения к базе данных (будет использовать SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем ненужное отслеживание изменений
db = SQLAlchemy(app)

# Модель для товара
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

# Инициализация базы данных
@app.before_request
def create_tables():
    db.create_all()

# Получение списка товаров
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()  # Получаем все товары из базы данных
    return jsonify([{'id': p.id, 'name': p.name} for p in products])

# Добавление нового товара
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()  # Получаем данные из тела запроса
    if not data or not data.get('name'):
        return jsonify({'error': 'Название товара обязательно'}), 400

    new_product = Product(name=data['name'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'id': new_product.id, 'name': new_product.name}), 201

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
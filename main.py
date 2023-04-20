from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Инициализация приложения
app = Flask(__name__)

# Конфиг базы
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phonebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Contact(db.Model):
    # Уникальный идентификатор контакта
    id = db.Column(db.Integer, primary_key=True)
    # Имя контакта
    name = db.Column(db.String(80), nullable=False)
    # Номер телефона контакта
    phone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        # Возвращает строку, представляющую объект контакта
        return f'<Contact {self.name}>'


# Переход на основную страницу
@app.route('/', methods=['GET', 'POST'])
def main():
    return redirect(url_for('index'))


# Добавление и чтение контактов
@app.route('/add', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        contact = Contact(name=name, phone=phone)
        db.session.add(contact)
        db.session.commit()
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)


# Удаление контактов
@app.route('/contacts/<int:contact_id>', methods=['POST', 'DELETE'])
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index'))


# Создание базы, если ее нет
with app.app_context() as c:
    db.create_all()

app.run()

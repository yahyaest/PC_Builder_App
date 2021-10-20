import os
from flask import Flask, render_template, request, redirect, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__,template_folder='Templates')
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PC_Component.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class PC_Component(db.Model):
    __tablename__ = "PC_Component"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='N/A')
    category = db.Column(db.String(50), nullable=False, default='N/A')
    sub_category = db.Column(db.String(50), nullable=False, default='N/A')
    component_type = db.Column(db.String(50), nullable=False, default='N/A')
    price = db.Column(db.Integer, nullable=False, default=0)
    rate = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, category, sub_category, component_type, price, rate):
        self.name = name
        self.category = category
        self.sub_category = sub_category
        self.component_type = component_type
        self.price = price
        self.rate = rate

    def __repr__(self):
        return 'Components Info ' + str(self.id)


class PC_ComponentSchema(ma.Schema):
    class Meta:
        fields = ("name", "category", "sub_category",
                  "component_type", "price", "rate")


class Orders(db.Model):
    __tablename__ = "ORDERS"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='N/A')
    mail = db.Column(db.String(50), nullable=False, default='N/A')
    bank = db.Column(db.String(50), nullable=False, default='N/A')
    price = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, mail, bank, price):
        self.name = name
        self.mail = mail
        self.bank = bank
        self.price = price

    def __repr__(self):
        return 'Orders Info ' + str(self.id)


class OrdersSchema(ma.Schema):
    class Meta:
        fields = ("name", "mail", "bank",
                  "price")


@app.route('/')
def home():

    return render_template('index.html')


@app.route('/main')
def main():

    name_list = []
    type_list = []
    price_list = []
    rate_list = []

    Components = PC_Component.query.all()
    for component in Components:
        name_list.append(component.name)
        type_list.append(component.component_type)
        price_list.append(component.price)
        rate_list.append(component.rate)

    # login = dict(zip(name_list, password_list))
    # login_data = jsonify({'access': login})

    return render_template('main.html', Components=Components, name_list=name_list, type_list=type_list, price_list=price_list, rate_list=rate_list)


@app.route('/table')
def table():
    Components = PC_Component.query.all()

    return render_template('table.html', Components=Components)


@app.route('/data')
def data():
    Components = PC_Component.query.all()
    Components_schema = PC_ComponentSchema(many=True)
    info = Components_schema.dump(Components).data
    return jsonify({'Components': info})


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        order.name = request.form['name']
        order.mail = request.form['mail']
        order.bank = request.form['bank']
        order.price = request.form['price']
        new_order = Orders(name=order.name, mail=order.mail,
                           bank=order.bank, price=order.price)
        db.session.add(new_order)
        db.session.commit()
        #print(name, mail, bank, price)

        return redirect('/order_message')
    else:
        name_list = []
        price_list = []
        Components = PC_Component.query.all()

        for component in Components:
            name_list.append(component.name)
            price_list.append(component.price)

        return render_template('order.html', Components=Components, name_list=name_list, price_list=price_list)


@app.route('/order_message')
def order_message():

    return render_template('order_message.html')


@app.route('/order_table')
def order_table():
    orders = Orders.query.all()

    return render_template('order_table.html', orders=orders)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True, host='0.0.0.0')

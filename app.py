import os
import psycopg2
import json
from flask import Flask, render_template, request, redirect, jsonify, json, Blueprint
from logger import setup_logging

environment = os.environ['ENV']
app_domain = os.environ['DOMAIN'] if environment == 'PROD' else ''
logger = setup_logging()

app_bp = Blueprint('app_bp', __name__,
    template_folder='templates',
    static_folder='static')

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='postgres',
                            database='pc_builder_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

def getComponent():
    try:
        logger.debug('Getting components from database')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM pc_component;')
        components = cur.fetchall()
        cur.close()
        conn.close()
        return components
    except Exception as e:
        logger.error(e)

def getOrders():
    try:
        logger.debug('Getting orders from database')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM orders;')
        orders = cur.fetchall()
        cur.close()
        conn.close()
        return orders
    except Exception as e:
        logger.error(e)

@app_bp.route('/')
def home():
    return render_template('index.html', app_domain=app_domain)


@app_bp.route('/main')
def main():
    name_list = []
    type_list = []
    price_list = []
    rate_list = []

    try:
        Components = getComponent()

        for component in Components:
            name_list.append(component[1])
            type_list.append(component[4])
            price_list.append(component[5])
            rate_list.append(component[6])
    except Exception as e:
        logger.error(e)
        Components = []

    return render_template('main.html', Components=Components, name_list=name_list, type_list=type_list, price_list=price_list, rate_list=rate_list, app_domain=app_domain)


@app_bp.route('/table')
def table():
    try:
        Components = getComponent()
    except Exception as e:
        logger.error(e)
        Components = []

    return render_template('table.html', Components=Components, app_domain=app_domain)


@app_bp.route('/data')
def data():
    try:
        Components = getComponent()
        info = json.dumps(Components)
    except Exception as e:
        logger.error(e)
        info = []

    return jsonify({'Components': info})


@app_bp.route('/order', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        logger.info('Creating order')
        name = request.form['name']
        mail = request.form['mail']
        bank = request.form['bank']
        price = request.form['price']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO orders (name, mail, bank, price)'
                    'VALUES (%s, %s, %s, %s)',
                    (name, mail, bank, price))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f'Order created successfully with name: {name}, mail: {mail}, bank: {bank}, price: {price}')

        return redirect(f'{app_domain}/order_message')
    else:
        name_list = []
        price_list = []
        try:
            Components = getComponent()

            for component in Components:
                name_list.append(component[1])
                price_list.append(component[5])

        except Exception as e:
            logger.error(e)
            Components = []

        return render_template('order.html', Components=Components, name_list=name_list, price_list=price_list, app_domain=app_domain)


@app_bp.route('/order_message')
def order_message():

    return render_template('order_message.html')


@app_bp.route('/order_table')
def order_table():
    try:
        orders = getOrders()

    except Exception as e:
        logger.error(e)
        orders = []

    return render_template('order_table.html', orders=orders, app_domain=app_domain)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    if environment == "PROD":
        app.register_blueprint(app_bp, url_prefix=app_domain)
    else:
        app.register_blueprint(app_bp)
    app.run(debug=True, host='0.0.0.0')

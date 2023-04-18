import os
import psycopg2
from flask import Flask, render_template, request, redirect, jsonify, json
import json

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='postgres',
                            database='pc_builder_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

def getComponent():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pc_component;')
    components = cur.fetchall()
    cur.close()
    conn.close()
    return components

def getOrders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders;')
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return orders

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/main')
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
        print(e)
        Components = []

    return render_template('main.html', Components=Components, name_list=name_list, type_list=type_list, price_list=price_list, rate_list=rate_list)


@app.route('/table')
def table():
    try:
        Components = getComponent()
    except Exception as e:
        print(e)
        Components = []

    return render_template('table.html', Components=Components)


@app.route('/data')
def data():
    try:
        Components = getComponent()
        info = json.dumps(Components)
    except Exception as e:
        print(e)
        info = []

    return jsonify({'Components': info})


@app.route('/order', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
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
        #print(name, mail, bank, price)

        return redirect('/order_message')
    else:
        name_list = []
        price_list = []
        try:
            Components = getComponent()

            for component in Components:
                name_list.append(component[1])
                price_list.append(component[5])

        except Exception as e:
            print(e)
            Components = []

        return render_template('order.html', Components=Components, name_list=name_list, price_list=price_list)


@app.route('/order_message')
def order_message():

    return render_template('order_message.html')


@app.route('/order_table')
def order_table():
    try:
        orders = getOrders()

    except Exception as e:
        print(e)
        orders = []

    return render_template('order_table.html', orders=orders)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True, host='0.0.0.0')

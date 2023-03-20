import os
import json
import psycopg2

conn = psycopg2.connect(
        host="postgres",
        database="pc_builder_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
conn.autocommit = True
cur = conn.cursor()

# Create Database
try:
    cur.execute('DROP DATABASE IF EXISTS pc_builder_db;')
    cur.execute('CREATE DATABASE pc_builder_db;')
except:
    print("DATABASE pc_builder_db already exist")

# Execute a command: this creates a new table
try:
    cur.execute('DROP TABLE IF EXISTS pc_component;')
    cur.execute('CREATE TABLE pc_component (id serial PRIMARY KEY,'
                                    'name varchar (150) NOT NULL,'
                                    'category varchar (50) NOT NULL,'
                                    'sub_category varchar (50) NOT NULL,'
                                    'component_type varchar (50) NOT NULL,'
                                    'price integer NOT NULL,'
                                    'rate integer NOT NULL);'
                                    )
except:
    print("TABLE pc_component already exist")

try:
    cur.execute('DROP TABLE IF EXISTS orders;')
    cur.execute('CREATE TABLE orders (id serial PRIMARY KEY,'
                                    'name varchar (150) NOT NULL,'
                                    'mail varchar (150) NOT NULL,'
                                    'bank varchar (50) NOT NULL,'
                                    'price integer NOT NULL);'
                                    )
except:
    print("TABLE orders already exist")


# Populate the pc_component table 
f=open('component.json',)
data = json.load(f)
for i in range(len(data)):
    cur.execute(f'INSERT INTO pc_component (name, category, sub_category, component_type, price, rate)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (data[i]["name"],
             data[i]["category"],
             data[i]["sub_category"],
             data[i]["component_type"],
             data[i]["price"],
             data[i]["rate"])
             )
f.close()

conn.commit()

cur.close()
conn.close()

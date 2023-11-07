import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import Flask, render_template, request, url_for, redirect


basedir = os.path.abspath(os.path.dirname(__file__)) # get the base directory of the project
app = Flask(__name__) # create the Flask app

DATABASE_NAME = 'real_estate_db' # name of the database to connect to

# Connection parameters, make sure to change these to your own settings
POSTGRES_URL = 'postgresql://real_estate_user:real_estate_password@db:5432'
DATABASE_URL = POSTGRES_URL + '/' + DATABASE_NAME

# Function to open a connection to the database
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Function to create a new database in PostgreSQL
def create_database(db_name):
    # Connection string to connect with the default 'postgres' database
    conn_string = POSTGRES_URL + '/postgres'

    # Connect to the PostgreSQL server
    conn = psycopg2.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- AUTOCOMMIT
    cursor = conn.cursor()

    # Check if the database already exists
    cursor.execute(psycopg2.sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"), (db_name,))
    exists = cursor.fetchone()

    # If the database does not exist, then create it
    if not exists:
        cursor.execute(psycopg2.sql.SQL("CREATE DATABASE {}").format(psycopg2.sql.Identifier(db_name)))

    cursor.close()
    conn.close()

# Function to create the database tables
def setup_db():
    # Create the database
    create_database(DATABASE_NAME)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id SERIAL PRIMARY KEY,
            location VARCHAR(255) NOT NULL,
            size INTEGER NOT NULL,
            rooms INTEGER NOT NULL,
            building_year INTEGER NOT NULL
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            date_of_birth DATE NOT NULL,
            phone_number VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS owners (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            date_of_birth DATE NOT NULL,
            phone_number VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            date_of_birth DATE NOT NULL,
            phone_number VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            owner_id INTEGER NOT NULL,
            agent_id INTEGER NOT NULL,
            price INTEGER NOT NULL,
            FOREIGN KEY (property_id) REFERENCES properties (id),
            FOREIGN KEY (client_id) REFERENCES clients (id),
            FOREIGN KEY (owner_id) REFERENCES owners (id),
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()


# show stuff
@app.route('/')
def show_property():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM properties;')
    properties = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('show_property.html', properties=properties)

@app.route('/show_client')
def show_client():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM clients;')
    clients = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('show_client.html', clients=clients)

@app.route('/show_owner')
def show_owner():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM owners;')
    owners = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('show_owner.html', owners=owners)

@app.route('/show_agent')
def show_agent():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM agents;')
    agents = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('show_agent.html', agents=agents)

@app.route('/show_contract')
def show_contract():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contracts;')
    contracts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('show_contract.html', contracts=contracts)


# create stuff
@app.route('/create_property', methods=['GET', 'POST'])
def create_property():
    if request.method == 'POST':
        location = request.form['location']
        size = request.form['size']
        rooms = request.form['rooms']
        building_year = request.form['building_year']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO properties (location, size, rooms, building_year) VALUES (%s, %s, %s, %s)',
                    (location, size, rooms, building_year))
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_property'))
    return render_template('create_property.html')

@app.route('/create_client', methods=['GET', 'POST'])
def create_client():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']
        address = request.form['address']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO clients (first_name, last_name, date_of_birth, phone_number, address) VALUES (%s, %s, %s, %s, %s)',
                    (first_name, last_name, date_of_birth, phone_number, address))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('show_client'))

    return render_template('create_client.html')

@app.route('/create_owner', methods=['GET', 'POST'])
def create_owner():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']
        address = request.form['address']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO owners (first_name, last_name, date_of_birth, phone_number, address) VALUES (%s, %s, %s, %s, %s)',
                    (first_name, last_name, date_of_birth, phone_number, address))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('show_owner'))

    return render_template('create_owner.html')

@app.route('/create_agent', methods=['GET', 'POST'])
def create_agent():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        email = request.form['email']
        phone_number = request.form['phone_number']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO agents (first_name, last_name, date_of_birth, email, phone_number) VALUES (%s, %s, %s, %s, %s)',
                    (first_name, last_name, date_of_birth, email, phone_number))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('show_agent'))

    return render_template('create_agent.html')

@app.route('/create_contract', methods=['GET', 'POST'])
def create_contract():
    if request.method == 'POST':
        property_id = request.form['property_id']
        agent_id = request.form['agent_id']
        client_id = request.form['client_id']
        owner_id = request.form['owner_id']
        contract_type = request.form['contract_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO contracts (property_id, agent_id, client_id, owner_id, contract_type, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (property_id, agent_id, client_id, owner_id, contract_type, start_date, end_date))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('show_contract'))

    return render_template('create_contract.html')

# Drop all tables
with app.app_context():
    setup_db()

if __name__ == '__main__':
    app.run(debug=True)
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import Flask, render_template, request, url_for, redirect
import logging

basedir = os.path.abspath(os.path.dirname(__file__)) # get the base directory of the project
app = Flask(__name__) # create the Flask app
app.logger.setLevel(logging.DEBUG)

DATABASE_NAME = 'real_estate_db' # name of the database to connect to

# Connection parameters, make sure to change these to your own settings
POSTGRES_URL = 'postgresql://real_estate_user:real_estate_password@db:5432'
DATABASE_URL = POSTGRES_URL + '/' + DATABASE_NAME

# Function to open a connection to the database
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

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
            phone_number VARCHAR(255) NOT NULL
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
        FOREIGN KEY (property_id) REFERENCES properties (id) ON DELETE CASCADE,
        FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE SET NULL,
        FOREIGN KEY (owner_id) REFERENCES owners (id) ON DELETE SET NULL,
        FOREIGN KEY (agent_id) REFERENCES agents (id) ON DELETE SET NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()


# Function to create a new database in PostgreSQL
def create_database(db_name):
    # Connection string to connect with the default 'postgres' database
    conn_string = POSTGRES_URL + '/postgres'

    # Connect to the PostgreSQL server
    conn = psycopg2.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- AUTOCOMMIT
    cursor = conn.cursor()

    # Check if the database already exists
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute(f"DROP DATABASE {db_name}")

    # If the database does not exist, then create it
    cursor.execute(f"CREATE DATABASE {db_name}")

    cursor.close()
    conn.close()

# fill database
def seed_db():
    print(11111)
    try:
        # Establish a connection to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert data into the properties table
        cur.execute('''
        INSERT INTO properties (location, size, rooms, building_year)
        VALUES
        ('123 Main St', 1000, 3, 1990),
        ('456 Elm St', 1500, 4, 1970),
        ('789 Maple St', 2000, 5, 1985);
        ''')

        # Insert data into the clients table
        cur.execute('''
        INSERT INTO clients (first_name, last_name, date_of_birth, phone_number, address)
        VALUES
        ('John', 'Doe', '1980-01-01', '1234567890', '123 Main St'),
        ('Jane', 'Smith', '1990-05-15', '0987654321', '456 Elm St');
        ''')

        # Insert data into the owners table
        cur.execute('''
        INSERT INTO owners (first_name, last_name, date_of_birth, phone_number, address)
        VALUES
        ('Alice', 'Johnson', '1975-09-30', '2345678901', '789 Maple St'),
        ('Bob', 'Brown', '1965-04-20', '8765432109', '101 Oak St');
        ''')

        # Insert data into the agents table
        cur.execute('''
        INSERT INTO agents (first_name, last_name, date_of_birth, phone_number)
        VALUES
        ('Charlie', 'Agent', '1985-07-11', '3456789012'),
        ('Diana', 'Broker', '1979-11-25', '5678901234');
        ''')

        # Insert data into the contracts table
        cur.execute('''
        INSERT INTO contracts (property_id, client_id, owner_id, agent_id, price)
        VALUES
        (1, 1, 1, 1, 100000),
        (2, 2, 2, 2, 150000);
        ''')

        # Commit the transaction
        conn.commit()

        print("Database seeded successfully.")

    except psycopg2.Error as e:
        # This catches PostgreSQL database related errors
        print(f"An error occurred while seeding the database: {e}")
    except Exception as e:
        # This catches non-database related errors
        print(f"An unexpected error occurred while seeding the database: {e}")
    finally:
        # Ensure that the cursor and connection are closed properly
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


# show stuff
@app.route('/')
def show_property():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM properties;')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    properties = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_property.html', properties=properties)

@app.route('/show_client')
def show_client():
    app.logger.debug('show_client')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM clients;')
    rows = cur.fetchall()

    columns = [desc[0] for desc in cur.description]

    # Convert list of tuples to list of dicts
    clients = [dict(zip(columns, row)) for row in rows]

    cur.close()
    conn.close()
    app.logger.debug(clients)
    return render_template('show_client.html', clients=clients)

@app.route('/show_owner')
def show_owner():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM owners;')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    owners = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_owner.html', owners=owners)

@app.route('/show_agent')
def show_agent():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM agents;')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    agents = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_agent.html', agents=agents)

@app.route('/show_contract')
def show_contract():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contracts;')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    contracts = [dict(zip(columns, row)) for row in rows]
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

with app.app_context():
    setup_db()  # Set up the database and create tables
    seed_db()   # Seed the database with initial data

if __name__ == '__main__':
    app.run(debug=True)
# ----- imports -----
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import Flask, render_template, request, url_for, redirect
import logging


# ----- set-up -----
basedir = os.path.abspath(os.path.dirname(__file__)) # get the base directory
app = Flask(__name__) # create the flask app
app.logger.setLevel(logging.DEBUG) # set the logging level to DEBUG


# connection parameters
DATABASE_NAME = 'real_estate_db' # name of the database 
POSTGRES_URL = 'postgresql://real_estate_user:real_estate_password@db:5432'
DATABASE_URL = POSTGRES_URL + '/' + DATABASE_NAME


# ----- definitions -----
# function to open a connection to the database
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# function to create the database tables
def setup_db(): 
    create_database(DATABASE_NAME) # create the database
    conn = get_db_connection() # open a connection to the database
    cur = conn.cursor() # create a cursor object

    # create address table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS address (
            address_id SERIAL PRIMARY KEY,
            street_number INTEGER,
            address_line VARCHAR(255),
            country VARCHAR(100),
            postal_code VARCHAR(20)
        );
    ''')

    # create person table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS person (
            person_id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            date_of_birth DATE NOT NULL,
            phone_number VARCHAR(20),
            email VARCHAR(255),
            address_id INTEGER,
            FOREIGN KEY (address_id) REFERENCES address(address_id)
        );
    ''')

    # create owner table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS owner (
            owner_id SERIAL PRIMARY KEY,
            person_id INTEGER NOT NULL,
            resident_status VARCHAR(50),
            acquisition_date DATE,
            FOREIGN KEY (person_id) REFERENCES person(person_id)
        );
    ''')

    # create agent table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS agent (
            agent_id SERIAL PRIMARY KEY,
            person_id INTEGER NOT NULL,
            employment_date DATE NOT NULL,
            FOREIGN KEY (person_id) REFERENCES person(person_id)
        );
    ''')

    # create client table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS client (
            client_id SERIAL PRIMARY KEY,
            person_id INTEGER NOT NULL,
            purchase_date DATE,
            FOREIGN KEY (person_id) REFERENCES person(person_id)
        );
    ''')

    # create location table
    cur.execute('''
            CREATE TABLE IF NOT EXISTS location (
                location_id SERIAL PRIMARY KEY,
                latitude DECIMAL NOT NULL,
                longitude DECIMAL NOT NULL
            );
        ''')

    # create property table with a foreign key reference to the location table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS property (
            property_id SERIAL PRIMARY KEY,
            number_of_rooms INTEGER,
            building_year INTEGER,
            area_size DECIMAL,
            price DECIMAL NOT NULL,
            location_id INTEGER, -- Foreign key reference to location table
            owner_id INTEGER NOT NULL, -- New column for owner_id
            FOREIGN KEY (location_id) REFERENCES location(location_id),
            FOREIGN KEY (owner_id) REFERENCES owner(owner_id) -- Foreign key reference to owner table
        );
    ''')

    # create contract table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS contract (
            contract_id SERIAL PRIMARY KEY,
            sign_date DATE NOT NULL,
            agent_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            property_id INTEGER NOT NULL,
            FOREIGN KEY (agent_id) REFERENCES agent(agent_id),
            FOREIGN KEY (client_id) REFERENCES client(client_id),
            FOREIGN KEY (property_id) REFERENCES property(property_id)
        );
    ''')

    # create payment table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS payment (
            payment_id SERIAL PRIMARY KEY,
            amount DECIMAL NOT NULL,
            date DATE NOT NULL,
            contract_id INTEGER NOT NULL,
            FOREIGN KEY (contract_id) REFERENCES contract(contract_id)
        );
    ''')

    # commt the changes to the database and close the connection
    conn.commit()
    cur.close()
    conn.close()


# function to create a new database with PostgreSQL
def create_database(db_name):
    conn_string = POSTGRES_URL + '/postgres' # connection string to connect with the default 'postgres' database

    # connect to the PostgreSQL server
    conn = psycopg2.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
    cursor = conn.cursor() # create a cursor object

    # check if the database already exists
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
    exists = cursor.fetchone()

    # if the database exists, drop it (remove the database)
    if exists:
        cursor.execute(f"DROP DATABASE {db_name}")

    # if the database does not exist, then create it
    cursor.execute(f"CREATE DATABASE {db_name}")

    cursor.close()
    conn.close()


# function to fill database
def seed_db():
    try:
        # establish a connection to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # insert data into the address table
        address_values = [
            (101, 'First St', 'Wonderland', '12345'),
            (202, 'Second St', 'Neverland', '23456'),
            (303, 'Third St', 'Oz', '34567'),
            (404, 'Fourth Ave', 'Narnia', '45678'),
            (505, 'Fifth Ave', 'Middle Earth', '56789'),
            (606, 'Sixth Blvd', 'Atlantis', '67890'),
            (707, 'Seventh Lane', 'El Dorado', '78901'),
            (808, 'Eighth Road', 'Shangri-La', '89012'),
            (909, 'Ninth Road', 'SNew York', '90012')
        ]
        cur.executemany('INSERT INTO address (street_number, address_line, country, postal_code) VALUES (%s, %s, %s, %s)', address_values)


        # insert data into the person table
        person_values = [
            ('Alice', 'Liddell', '1985-05-04', '1112223333', 'alice@example.com', 1),
            ('Peter', 'Pan', '1986-06-04', '2223334444', 'peter@example.com', 2),
            ('Dorothy', 'Gale', '1987-07-04', '3334445555', 'dorothy@example.com', 3),
            ('Wendy', 'Darling', '1988-08-04', '4445556666', 'wendy@example.com', 4),
            ('Harry', 'Potter', '1989-09-04', '5556667777', 'harry@example.com', 5),
            ('Hermione', 'Granger', '1990-10-04', '6667778888', 'hermione@example.com', 6),
            ('Ron', 'Weasley', '1991-11-04', '7778889999', 'ron@example.com', 7),
            ('Luke', 'Skywalker', '1992-12-04', '8889990000', 'luke@example.com', 8),
            ('Henry', 'Potter', '1999-12-04', '8887990000', 'henry@example.com', 9)
        ]
        cur.executemany('INSERT INTO person (first_name, last_name, date_of_birth, phone_number, email, address_id) VALUES (%s, %s, %s, %s, %s, %s)', person_values)

        # insert data into the owner table
        owner_values = [
            (1, 'Permanent', '2001-01-01'),
            (2, 'Temporary', '2002-02-02'),
            (3, 'Permanent', '2003-03-03')
        ]
        cur.executemany('INSERT INTO owner (person_id, resident_status, acquisition_date) VALUES (%s, %s, %s)', owner_values)

        # insert data into the agent table
        agent_values = [
            (4, '2010-01-01'),
            (5, '2011-02-01'),
            (6, '2012-01-01')
        ]
        cur.executemany('INSERT INTO agent (person_id, employment_date) VALUES (%s, %s)', agent_values)

        # insert data into the client table
        client_values = [
            (7, '2020-01-01'),
            (8, '2021-02-01'),
            (9, '2022-01-01')
        ]
        cur.executemany('INSERT INTO client (person_id, purchase_date) VALUES (%s, %s)', client_values)

        # insert sample data into the location table
        location_values = [
            (40.712776, -74.005974), 
            (34.052235, -118.243683),  
            (51.507351, -0.127758),  
            (35.689487, 139.691706),  
            (48.856614, 2.352222),  
            (55.755826, 37.617300), 
            (-33.868820, 151.209296),  
            (-23.550520, -46.633309),  
            (52.520007, 13.404954)
        ]
        cur.executemany('INSERT INTO location (latitude, longitude) VALUES (%s, %s)', location_values)


        # insert data into the property table
        property_values = [
            (3, 1990, 100.0, 200000.0, 1, 1),
            (4, 1980, 150.0, 250000.0, 2, 2),
            (5, 2000, 200.0, 300000.0, 3, 3),
            (2, 2010, 120.0, 180000.0, 4, 1),
            (6, 1975, 250.0, 400000.0, 5, 2),
            (1, 2020, 80.0,  150000.0, 6, 3),
            (3, 1950, 90.0,  220000.0, 7, 1),
            (4, 1995, 180.0, 350000.0, 8, 2),
            (5, 1985, 160.0, 275000.0, 9, 3)
        ]
        cur.executemany('INSERT INTO property (number_of_rooms, building_year, area_size, price, location_id, owner_id) VALUES (%s, %s, %s, %s, %s, %s)', property_values)

         # insert data into the contract table
        contract_values = [
            ('2022-01-01', 1, 1, 1),
            ('2022-02-01', 2, 2, 2),
            ('2022-03-01', 3, 3, 3),
            ('2022-04-01', 1, 1, 4),
            ('2022-05-01', 2, 2, 5),
            ('2022-06-01', 3, 3, 6),
            ('2022-07-01', 1, 1, 7),
            ('2022-08-01', 2, 2, 8),
            ('2022-09-01', 3, 3, 9)
        ]
        cur.executemany('INSERT INTO contract (sign_date, agent_id, client_id, property_id) VALUES (%s, %s, %s, %s)', contract_values)


        # insert data into the payment table
        payment_values = [
            (100000.0, '2022-01-05', 1),
            (150000.0, '2022-02-05', 2),
            (200000.0, '2022-03-05', 3),
            (175000.0, '2022-04-06', 4),
            (225000.0, '2022-05-07', 5),
            (120000.0, '2022-06-08', 6),
            (160000.0, '2022-07-09', 7),
            (210000.0, '2022-08-10', 8),
            (190000.0, '2022-09-11', 9)
        ]
        cur.executemany('INSERT INTO payment (amount, date, contract_id) VALUES (%s, %s, %s)', payment_values)

        # commit the transaction
        conn.commit()

        print("Database seeded successfully.")

    # Exception handling
    except psycopg2.Error as e:
        # this catches PostgreSQL database related errors
        print(f"An error occurred while seeding the database: {e}")
    except Exception as e:
        # this catches non-database related errors
        print(f"An unexpected error occurred while seeding the database: {e}")
        raise e
    finally:
        # ensure that the cursor and connection are closed properly
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


# ------- show stuff -------
# show home
@app.route('/')
def home():
    # redirect to about-us
    return redirect('/about-us ')

# show about-us
@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

# show address
@app.route('/show_address')
def show_address():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all address entries
    cur.execute('SELECT * FROM address;')
    rows = cur.fetchall() # fetch all rows returned by the query

    # extract the column names from the cursor object
    columns = [desc[0] for desc in cur.description]

    # combine the column names and row values into a list of dictionaries
    address_entries = [dict(zip(columns, row)) for row in rows]

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('show_address.html', address_entries=address_entries)


# show person
@app.route('/show_person')
def show_person():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all person entries and relevant columns from the address table, joining them on the address_id
    cur.execute('''
        SELECT p.*, a.address_line, a.country, a.postal_code 
        FROM person p
        JOIN address a ON p.address_id = a.address_id;
    ''')
    rows = cur.fetchall() # fetch all rows returned by the query

    # extract the column names from the cursor object
    columns = [desc[0] for desc in cur.description]

    # combine the column names and row values into a list of dictionaries
    persons = [dict(zip(columns, row)) for row in rows]

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('show_person.html', persons=persons)


# show owner
@app.route('/show_owner')
def show_owner():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all owner entries and relevant columns from the person and address table, joining them on the person_id and address_id
    cur.execute('''
        SELECT o.*, p.first_name, p.last_name, p.email, p.date_of_birth, p.phone_number, a.address_line 
        FROM owner o
        JOIN person p ON o.person_id = p.person_id
        JOIN address a ON p.address_id = a.address_id;
    ''')
    rows = cur.fetchall() # fetch all rows returned by the query

    # extract the column names from the cursor object
    columns = [desc[0] for desc in cur.description]

    # combine the column names and row values into a list of dictionaries
    owners = [dict(zip(columns, row)) for row in rows]

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('show_owner.html', owners=owners)


# show agent
@app.route('/show_agent')
def show_agent():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all agent entries and relevant columns from the person and address table, joining them on the person_id and address_id
    cur.execute('''
        SELECT ag.*, p.first_name, p.last_name, p.email, p.date_of_birth, p.phone_number, a.address_line 
        FROM agent ag
        JOIN person p ON ag.person_id = p.person_id
        JOIN address a ON p.address_id = a.address_id;
    ''')
    rows = cur.fetchall() # fetch all rows returned by the query

    # extract the column names from the cursor object
    columns = [desc[0] for desc in cur.description]

    # combine the column names and row values into a list of dictionaries
    agents = [dict(zip(columns, row)) for row in rows]

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('show_agent.html', agents=agents)


# show client
@app.route('/show_client')
def show_client():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all client entries and relevant columns from the person and address table, joining them on the person_id and address_id
    cur.execute('''
        SELECT cl.*, p.first_name, p.last_name, p.email, p.date_of_birth, p.phone_number, a.address_line 
        FROM client cl
        JOIN person p ON cl.person_id = p.person_id
        JOIN address a ON p.address_id = a.address_id;
    ''')
    rows = cur.fetchall() # fetch all rows returned by the query

    # extract the column names from the cursor object
    columns = [desc[0] for desc in cur.description]

    # combine the column names and row values into a list of dictionaries
    clients = [dict(zip(columns, row)) for row in rows]

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('show_client.html', clients=clients)


# show location
@app.route('/show_location')
def show_location():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all location entries
    cur.execute('SELECT * FROM location;')
    rows = cur.fetchall() # fetch all rows returned by the query

    # extract the column names from the cursor object
    columns = [desc[0] for desc in cur.description]

    # combine the column names and row values into a list of dictionaries
    locations = [dict(zip(columns, row)) for row in rows]

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('show_location.html', locations=locations)


# show property
@app.route('/show_property')
def show_property():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()
    
    # select all property entries and relevant columns from the location, owner, and person table, joining them on the location_id, owner_id, and person_id
    cur.execute('''
        SELECT p.*, per.first_name, per.last_name, l.latitude, l.longitude
        FROM property p
        JOIN location l ON p.location_id = l.location_id
        JOIN owner o ON p.owner_id = o.owner_id
        JOIN person per ON o.person_id = per.person_id;  -- Join with person table to get owner name
    ''')
    rows = cur.fetchall() # fetch all rows returned by the query

    # extract the column names from the cursor object
    columns = [desc[0] for desc in cur.description]

    # combine the column names and row values into a list of dictionaries
    properties = [dict(zip(columns, row)) for row in rows]

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('show_property.html', properties=properties)

# show contract
@app.route('/show_contract')
def show_contract():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all contract entries and relevant columns from the agent, client, property, and location table, joining them on the agent_id, client_id, property_id, and location_id
    cur.execute('''
        SELECT c.contract_id, c.sign_date, 
               a.first_name AS agent_first_name, a.last_name AS agent_last_name, 
               cl.first_name AS client_first_name, cl.last_name AS client_last_name, 
               p.property_id, l.latitude, l.longitude
        FROM contract c
        JOIN agent ag ON c.agent_id = ag.agent_id
        JOIN person a ON ag.person_id = a.person_id
        JOIN client clt ON c.client_id = clt.client_id
        JOIN person cl ON clt.person_id = cl.person_id
        JOIN property p ON c.property_id = p.property_id
        JOIN location l ON p.location_id = l.location_id;
    ''')
    rows = cur.fetchall() # fetch all rows returned by the query

    # extract the column names from the cursor object
    columns = [desc[0] for desc in cur.description]

    # combine the column names and row values into a list of dictionaries
    contracts = [dict(zip(columns, row)) for row in rows]

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('show_contract.html', contracts=contracts)

# show payment
@app.route('/show_payment')
def show_payment():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all payment entries and relevant columns from the contract table, joining them on the contract_id
    cur.execute('''
        SELECT p.*, c.contract_id 
        FROM payment p
        JOIN contract c ON p.contract_id = c.contract_id;
    ''')
    rows = cur.fetchall() # fetch all rows returned by the query

    # extract the column names from the cursor object
    columns = [desc[0] for desc in cur.description]

    # combine the column names and row values into a list of dictionaries
    payments = [dict(zip(columns, row)) for row in rows]

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('show_payment.html', payments=payments)


# ------- create stuff --------
# create address
@app.route('/create_address', methods=['GET', 'POST'])
def create_address():
    # check if the request method is POST, which means the form has been submitted
    if request.method == 'POST':
        # retrieve form data from the request object
        street_number = request.form['street_number']
        address_line = request.form['address_line']
        country = request.form['country']
        postal_code = request.form['postal_code']
        
        # establish a database connection and create a cursor object
        conn = get_db_connection()
        cur = conn.cursor()

        # insert the form data into the address table
        cur.execute('INSERT INTO address (street_number, address_line, country, postal_code) VALUES (%s, %s, %s, %s)',
                    (street_number, address_line, country, postal_code))

        # commit changes to the database and close the cursor and connection
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_address'))
    return render_template('create_address.html')

# create person
@app.route('/create_person', methods=['GET', 'POST'])
def create_person():
    # check if the request method is POST, which means the form has been submitted
    if request.method == 'POST':
        # retrieve form data from the request object
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address_id = request.form['address_id'] 
        
        # establish a database connection and create a cursor object
        conn = get_db_connection()
        cur = conn.cursor()

        # insert the form data into the person table
        cur.execute('''
            INSERT INTO person (first_name, last_name, date_of_birth, phone_number, email, address_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (first_name, last_name, date_of_birth, phone_number, email, address_id))

        # commit changes to the database and close the cursor and connection
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_person'))
  
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all address entries from the address table
    cur.execute('SELECT address_id, address_line FROM address;')

    # fetch all rows returned by the query and close the cursor and connection
    addresses = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('create_person.html', addresses=addresses)

# create owner
@app.route('/create_owner', methods=['GET', 'POST'])
def create_owner():
    # check if the request method is POST, which means the form has been submitted
    if request.method == 'POST':
        # retrieve form data from the request object
        person_id = request.form['person_id'] 
        resident_status = request.form['resident_status']
        acquisition_date = request.form['acquisition_date']
        
        # establish a database connection and create a cursor object
        conn = get_db_connection()
        cur = conn.cursor()

        # insert the form data into the owner table
        cur.execute('''
            INSERT INTO owner (person_id, resident_status, acquisition_date) 
            VALUES (%s, %s, %s)
        ''', (person_id, resident_status, acquisition_date))

        # commit changes to the database and close the cursor and connection
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_owner'))

    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all person entries from the person table
    cur.execute('SELECT person_id, first_name, last_name FROM person;')

    # fetch all rows returned by the query and close the cursor and connection
    persons = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('create_owner.html', persons=persons)

# create agent
@app.route('/create_agent', methods=['GET', 'POST'])
def create_agent():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # check if the request method is POST, which means the form has been submitted
    if request.method == 'POST':
        # retrieve form data from the request object
        person_id = request.form['person_id']
        employment_date = request.form['employment_date']

        # insert the form data into the agent table
        cur.execute('''
            INSERT INTO agent (person_id, employment_date) 
            VALUES (%s, %s)
        ''', (person_id, employment_date))
        conn.commit() # commit changes to the database

    # select all person entries from the person table
    cur.execute('SELECT person_id, first_name, last_name FROM person;')

    # fetch all rows returned by the query and close the cursor and connection
    persons = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('create_agent.html', persons=persons)

# create client
@app.route('/create_client', methods=['GET', 'POST'])
def create_client():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all person entries from the person table
    cur.execute('SELECT person_id, first_name, last_name FROM person;')
    persons = cur.fetchall() # fetch all rows returned by the query

    # check if the request method is POST, which means the form has been submitted
    if request.method == 'POST':
        # retrieve form data from the request object
        person_id = request.form['person_id']
        purchase_date = request.form['purchase_date']

        # insert the form data into the client table
        cur.execute('''
            INSERT INTO client (person_id, purchase_date) 
            VALUES (%s, %s)
        ''', (person_id, purchase_date))
        conn.commit() # commit changes to the database

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('create_client.html', persons=persons)

# create location
@app.route('/create_location', methods=['GET', 'POST'])
def create_location():
    # check if the request method is POST, which means the form has been submitted
    if request.method == 'POST':
        # retrieve form data from the request object
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        # establish a database connection and create a cursor object
        conn = get_db_connection()
        cur = conn.cursor()

        # insert the form data into the location table
        cur.execute('INSERT INTO location (latitude, longitude) VALUES (%s, %s)',
                    (latitude, longitude))

        # commit changes to the database and close the cursor and connection
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_location')) 
    return render_template('create_location.html')

# create property
@app.route('/create_property', methods=['GET', 'POST'])
def create_property():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all location entries from the location table
    cur.execute('SELECT location_id, latitude, longitude FROM location;')
    locations = cur.fetchall() # fetch all rows returned by the query

    # select all owner entries from the owner table
    cur.execute('''
        SELECT o.owner_id, p.first_name || ' ' || p.last_name AS owner_name
        FROM owner o
        JOIN person p ON o.person_id = p.person_id;
    ''')
    owners = cur.fetchall() # fetch all rows returned by the query
    
    # check if the request method is POST, which means the form has been submitted
    if request.method == 'POST':
        # retrieve form data from the request object
        number_of_rooms = request.form['number_of_rooms']
        building_year = request.form['building_year']
        area_size = request.form['area_size']
        price = request.form['price']
        location_id = request.form['location_id']
        owner_id = request.form['owner_id'] 

        # insert the form data into the property table
        cur.execute('''
            INSERT INTO property (number_of_rooms, building_year, area_size, price, location_id, owner_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (number_of_rooms, building_year, area_size, price, location_id, owner_id))

        # commit changes to the database and close the cursor and connection
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_property'))

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('create_property.html', locations=locations, owners=owners)


# create contract
@app.route('/create_contract', methods=['GET', 'POST'])
def create_contract():
    # check if the request method is POST, which means the form has been submitted
    if request.method == 'POST':
        # retrieve form data from the request object
        sign_date = request.form['sign_date']
        agent_id = request.form['agent_id']
        client_id = request.form['client_id']
        property_id = request.form['property_id']
        
        # establish a database connection and create a cursor object
        conn = get_db_connection()
        cur = conn.cursor()

        # insert the form data into the contract table
        cur.execute('''
            INSERT INTO contract (sign_date, agent_id, client_id, property_id) 
            VALUES (%s, %s, %s, %s)
        ''', (sign_date, agent_id, client_id, property_id))

        # commit changes to the database and close the cursor and connection
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_contract'))

    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all agent, client and property entries from the agent, client and property tables
    cur.execute('SELECT agent_id, first_name, last_name FROM agent JOIN person ON agent.person_id = person.person_id;')
    agents = cur.fetchall()
    cur.execute('SELECT client_id, first_name, last_name FROM client JOIN person ON client.person_id = person.person_id;')
    clients = cur.fetchall()
    cur.execute('SELECT property_id, location FROM property;')

    # fetch all rows returned by the query and close the cursor and connection
    properties = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('create_contract.html', agents=agents, clients=clients, properties=properties)

# create payment
@app.route('/create_payment', methods=['GET', 'POST'])
def create_payment():
    # establish a database connection and create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()

    # select all contract entries from the contract table
    if request.method == 'POST':
        amount = request.form['amount']
        date = request.form['date']
        contract_id = request.form['contract_id']
        
        # insert the form data into the payment table
        cur.execute('''
            INSERT INTO payment (amount, date, contract_id) 
            VALUES (%s, %s, %s)
        ''', (amount, date, contract_id))
        conn.commit() # commit changes to the database

    # select all contract entries from the contract table
    cur.execute('SELECT contract_id FROM contract;')
    contracts = cur.fetchall() # fetch all rows returned by the query

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('create_payment.html', contracts=contracts)


with app.app_context():
    setup_db()  # set up the database and create tables
    seed_db()   # seed the database with initial data

if __name__ == '__main__':
    app.run(debug=True)
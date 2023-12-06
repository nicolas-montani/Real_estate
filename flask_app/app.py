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

    # Create address table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS address (
            address_id SERIAL PRIMARY KEY,
            street_number INTEGER,
            address_line VARCHAR(255),
            country VARCHAR(100),
            postal_code VARCHAR(20)
        );
    ''')

    # Create person table
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

    # Create owner table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS owner (
            owner_id SERIAL PRIMARY KEY,
            person_id INTEGER NOT NULL,
            resident_status VARCHAR(50),
            acquisition_date DATE,
            FOREIGN KEY (person_id) REFERENCES person(person_id)
        );
    ''')

    # Create agent table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS agent (
            agent_id SERIAL PRIMARY KEY,
            person_id INTEGER NOT NULL,
            employment_date DATE NOT NULL,
            manages INTEGER,  -- Assuming this is a reference to another agent ID
            FOREIGN KEY (person_id) REFERENCES person(person_id)
        );
    ''')

    # Create client table
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

    # Create contract table
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

    # Create payment table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS payment (
            payment_id SERIAL PRIMARY KEY,
            amount DECIMAL NOT NULL,
            date DATE NOT NULL,
            contract_id INTEGER NOT NULL,
            FOREIGN KEY (contract_id) REFERENCES contract(contract_id)
        );
    ''')

    # Commit the changes to the database
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


# Function to fill database
def seed_db():
    try:
        # Establish a connection to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert data into the address table
        address_values = [
            (101, 'First St', 'Wonderland', '12345'),
            (202, 'Second St', 'Neverland', '23456'),
            (303, 'Third St', 'Oz', '34567'),
        ]
        cur.executemany('INSERT INTO address (street_number, address_line, country, postal_code) VALUES (%s, %s, %s, %s)', address_values)

        # Insert data into the person table
        person_values = [
            ('Alice', 'Liddell', '1985-05-04', '1112223333', 'alice@example.com', 1),
            ('Peter', 'Pan', '1986-06-04', '2223334444', 'peter@example.com', 2),
            ('Dorothy', 'Gale', '1987-07-04', '3334445555', 'dorothy@example.com', 3),
        ]
        cur.executemany('INSERT INTO person (first_name, last_name, date_of_birth, phone_number, email, address_id) VALUES (%s, %s, %s, %s, %s, %s)', person_values)

        # Insert data into the owner table
        owner_values = [
            (1, 'Permanent', '2001-01-01'),
            (2, 'Permanent', '2002-02-02'),
            (3, 'Permanent', '2003-03-03'),
        ]
        cur.executemany('INSERT INTO owner (person_id, resident_status, acquisition_date) VALUES (%s, %s, %s)', owner_values)

        # Insert data into the agent table
        agent_values = [
            (1, '2010-01-01'),
            (2, '2011-01-01'),
            (3, '2012-01-01'),
        ]
        cur.executemany('INSERT INTO agent (person_id, employment_date) VALUES (%s, %s)', agent_values)

        # Insert data into the client table
        client_values = [
            (1, '2020-01-01'),
            (2, '2021-01-01'),
            (3, '2022-01-01'),
        ]
        cur.executemany('INSERT INTO client (person_id, purchase_date) VALUES (%s, %s)', client_values)

        # Insert sample data into the location table
        location_values = [
            (40.712776, -74.005974),  # Latitude and longitude for New York City
            (34.052235, -118.243683),  # Latitude and longitude for Los Angeles
            (51.507351, -0.127758),    # Latitude and longitude for London
        ]
        cur.executemany('INSERT INTO location (latitude, longitude) VALUES (%s, %s)', location_values)


        # Insert data into the property table
        # Assuming the first three location_ids are for the locations inserted above
        property_values = [
            (3, 1990, 100.0, 200000.0, 1, 1),  
            (4, 1980, 150.0, 250000.0, 2, 2),  
            (5, 2000, 200.0, 300000.0, 3, 3),  
        ]
        cur.executemany('INSERT INTO property (number_of_rooms, building_year, area_size, price, location_id, owner_id) VALUES (%s, %s, %s, %s, %s, %s)', property_values)

         # Insert data into the contract table
        contract_values = [
            ('2022-01-01', 1, 1, 1),
            ('2022-02-01', 2, 2, 2),
            ('2022-03-01', 3, 3, 3),
        ]
        cur.executemany('INSERT INTO contract (sign_date, agent_id, client_id, property_id) VALUES (%s, %s, %s, %s)', contract_values)


        # Insert data into the payment table
        payment_values = [
            (100000.0, '2022-01-05', 1),
            (150000.0, '2022-02-05', 2),
            (200000.0, '2022-03-05', 3),
        ]
        cur.executemany('INSERT INTO payment (amount, date, contract_id) VALUES (%s, %s, %s)', payment_values)

        # Commit the transaction
        conn.commit()

        print("Database seeded successfully.")

    except psycopg2.Error as e:
        # This catches PostgreSQL database related errors
        print(f"An error occurred while seeding the database: {e}")
    except Exception as e:
        # This catches non-database related errors
        print(f"An unexpected error occurred while seeding the database: {e}")
        raise e
    finally:
        # Ensure that the cursor and connection are closed properly
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


# ------- show stuff -------

# show home
@app.route('/')
def home():
    #redirect to about-us
    return redirect('/about-us ')

# show about-us
@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

# show address
@app.route('/show_address')
def show_address():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM address;')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    address_entries = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_address.html', address_entries=address_entries)


# show person
@app.route('/show_person')
def show_person():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT p.*, a.address_line, a.country, a.postal_code 
        FROM person p
        JOIN address a ON p.address_id = a.address_id;
    ''')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    persons = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_person.html', persons=persons)


# show owner
@app.route('/show_owner')
def show_owner():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT o.*, p.first_name, p.last_name, p.email, p.date_of_birth, p.phone_number, a.address_line 
        FROM owner o
        JOIN person p ON o.person_id = p.person_id
        JOIN address a ON p.address_id = a.address_id;
    ''')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    owners = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_owner.html', owners=owners)


# show agent
@app.route('/show_agent')
def show_agent():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT ag.*, p.first_name, p.last_name, p.email, p.date_of_birth, p.phone_number, a.address_line 
        FROM agent ag
        JOIN person p ON ag.person_id = p.person_id
        JOIN address a ON p.address_id = a.address_id;
    ''')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    agents = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_agent.html', agents=agents)

# show client
@app.route('/show_client')
def show_client():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT cl.*, p.first_name, p.last_name, p.email, p.date_of_birth, p.phone_number, a.address_line 
        FROM client cl
        JOIN person p ON cl.person_id = p.person_id
        JOIN address a ON p.address_id = a.address_id;
    ''')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    clients = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_client.html', clients=clients)

# show location
@app.route('/show_location')
def show_location():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM location;')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    locations = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_location.html', locations=locations)


# show property
@app.route('/show_property')
def show_property():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT p.*, per.first_name, per.last_name, l.latitude, l.longitude
        FROM property p
        JOIN location l ON p.location_id = l.location_id
        JOIN owner o ON p.owner_id = o.owner_id
        JOIN person per ON o.person_id = per.person_id;  -- Join with person table to get owner name
    ''')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    properties = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_property.html', properties=properties)



@app.route('/show_contract')
def show_contract():
    conn = get_db_connection()
    cur = conn.cursor()
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
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    contracts = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_contract.html', contracts=contracts)

# show payment
@app.route('/show_payment')
def show_payment():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT p.*, c.contract_id 
        FROM payment p
        JOIN contract c ON p.contract_id = c.contract_id;
    ''')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    payments = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return render_template('show_payment.html', payments=payments)





# ------- create stuff --------
# create address
@app.route('/create_address', methods=['GET', 'POST'])
def create_address():
    if request.method == 'POST':
        street_number = request.form['street_number']
        address_line = request.form['address_line']
        country = request.form['country']
        postal_code = request.form['postal_code']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO address (street_number, address_line, country, postal_code) VALUES (%s, %s, %s, %s)',
                    (street_number, address_line, country, postal_code))
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_address'))
    return render_template('create_address.html')

# create person
@app.route('/create_person', methods=['GET', 'POST'])
def create_person():
    if request.method == 'POST':
        #person_id = request.form['person_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address_id = request.form['address_id']  # Make sure this is a valid ID from the address table
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO person (first_name, last_name, date_of_birth, phone_number, email, address_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (first_name, last_name, date_of_birth, phone_number, email, address_id))
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_person'))
    # Provide a list of addresses for the dropdown
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT address_id, address_line FROM address;')
    addresses = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('create_person.html', addresses=addresses)

# create owner
@app.route('/create_owner', methods=['GET', 'POST'])
def create_owner():
    if request.method == 'POST':
        person_id = request.form['person_id']  # Make sure this is a valid ID from the person table
        resident_status = request.form['resident_status']
        acquisition_date = request.form['acquisition_date']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO owner (person_id, resident_status, acquisition_date) 
            VALUES (%s, %s, %s)
        ''', (person_id, resident_status, acquisition_date))
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_owner'))

    # Provide a list of persons for the dropdown
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT person_id, first_name, last_name FROM person;')
    persons = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('create_owner.html', persons=persons)

# create agent
@app.route('/create_agent', methods=['GET', 'POST'])
def create_agent():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        person_id = request.form['person_id']
        employment_date = request.form['employment_date']

        # Insert into agent table with the existing person_id
        cur.execute('''
            INSERT INTO agent (person_id, employment_date) 
            VALUES (%s, %s)
        ''', (person_id, employment_date))
        conn.commit()

    # Fetch persons for the dropdown
    cur.execute('SELECT person_id, first_name, last_name FROM person;')
    persons = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('create_agent.html', persons=persons)

# create client
@app.route('/create_client', methods=['GET', 'POST'])
def create_client():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch persons for the dropdown
    cur.execute('SELECT person_id, first_name, last_name FROM person;')
    persons = cur.fetchall()

    if request.method == 'POST':
        person_id = request.form['person_id']
        purchase_date = request.form['purchase_date']

        # Insert into client table with the existing person_id
        cur.execute('''
            INSERT INTO client (person_id, purchase_date) 
            VALUES (%s, %s)
        ''', (person_id, purchase_date))
        conn.commit()

    cur.close()
    conn.close()

    return render_template('create_client.html', persons=persons)

# create location
@app.route('/create_location', methods=['GET', 'POST'])
def create_location():
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO location (latitude, longitude) VALUES (%s, %s)',
                    (latitude, longitude))
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_location'))  # Redirect to a page that shows all locations
    return render_template('create_location.html')

# create property
@app.route('/create_property', methods=['GET', 'POST'])
def create_property():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT location_id, latitude, longitude FROM location;')
    locations = cur.fetchall()
    
    if request.method == 'POST':
        number_of_rooms = request.form['number_of_rooms']
        building_year = request.form['building_year']
        area_size = request.form['area_size']
        price = request.form['price']
        location_id = request.form['location_id']  # Get location_id from the form
        
        cur.execute('''
            INSERT INTO property (number_of_rooms, building_year, area_size, price, location_id) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (number_of_rooms, building_year, area_size, price, location_id))
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_property'))
    cur.close()
    conn.close()
    return render_template('create_property.html', locations=locations)


# create contract
@app.route('/create_contract', methods=['GET', 'POST'])
def create_contract():
    if request.method == 'POST':
        sign_date = request.form['sign_date']
        agent_id = request.form['agent_id']
        client_id = request.form['client_id']
        property_id = request.form['property_id']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO contract (sign_date, agent_id, client_id, property_id) 
            VALUES (%s, %s, %s, %s)
        ''', (sign_date, agent_id, client_id, property_id))
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('show_contract'))

    # Fetching lists of agents, clients, and properties for the dropdowns
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT agent_id, first_name, last_name FROM agent JOIN person ON agent.person_id = person.person_id;')
    agents = cur.fetchall()
    cur.execute('SELECT client_id, first_name, last_name FROM client JOIN person ON client.person_id = person.person_id;')
    clients = cur.fetchall()
    cur.execute('SELECT property_id, location FROM property;')
    properties = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('create_contract.html', agents=agents, clients=clients, properties=properties)

# create payment
@app.route('/create_payment', methods=['GET', 'POST'])
def create_payment():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        amount = request.form['amount']
        date = request.form['date']
        contract_id = request.form['contract_id']
        
        cur.execute('''
            INSERT INTO payment (amount, date, contract_id) 
            VALUES (%s, %s, %s)
        ''', (amount, date, contract_id))
        conn.commit()

    # Fetch contracts for the dropdown
    cur.execute('SELECT contract_id FROM contract;')
    contracts = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('create_payment.html', contracts=contracts)


with app.app_context():
    setup_db()  # Set up the database and create tables
    seed_db()   # Seed the database with initial data

if __name__ == '__main__':
    app.run(debug=True)
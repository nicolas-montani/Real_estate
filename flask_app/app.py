import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.sql')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Property(db.Model):
    __tablename__ = 'propertys'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer)
    rooms = db.Column(db.Float)
    building_year = db.Column(db.Integer) 

    # Define the 'contracts' relationship
    contracts = db.relationship('Contract', back_populates='property')

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String)

    # Define the 'contracts' relationship
    contracts = db.relationship('Contract', back_populates='client')
    
    
class Owner(db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String)

    # Define the 'contracts' relationship
    contracts = db.relationship('Contract', back_populates='owner')

class Agent(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer)

    # Define the 'contracts' relationship
    contracts = db.relationship('Contract', back_populates='agent')

class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('propertys.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    contract_type = db.Column(db.String)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String)

    property = db.relationship('Property', back_populates='contracts')
    agent = db.relationship('Agent', back_populates='contracts')
    client = db.relationship('Client', back_populates='contracts')
    owner = db.relationship('Owner', back_populates='contracts')

#####show stuff ########
@app.route('/')
def show_property():
    properties = Property.query.all()
    return render_template('show_property.html', properties=properties)

@app.route('/show_client')
def show_client():
    clients = Client.query.all()
    return render_template('show_client.html', clients=clients)

@app.route('/show_owner')
def show_owner():
    owners = Owner.query.all()
    return render_template('show_owner.html', owners=owners)

@app.route('/show_agent')
def show_agent():
    agents = Agent.query.all()
    return render_template('show_agent.html', agents=agents)


@app.route('/show_contract')
def show_contract():
    # Retrieve all contracts from the database
    contracts = Contract.query.all()
    return render_template('show_contract.html', contracts=contracts)

######create stuff########
@app.route('/create_property', methods=['GET', 'POST'])
def create_property():
    if request.method == 'POST':
        location = request.form['location']
        size = request.form['size']
        rooms = request.form['rooms']
        building_year = request.form['building_year']

        # Create a new Property object and add it to the database
        property = Property(location=location, size=size, rooms=rooms, building_year=building_year)
        db.session.add(property)
        db.session.commit()

        return redirect(url_for('show_property'))

    return render_template('create_property.html')

@app.route('/create_client', methods=['GET', 'POST'])
def create_client():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = str(request.form['date_of_birth'])
        phone_number = request.form['phone_number']
        address = request.form['address']

        # Create a new Client object and add it to the database
        client = Client(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, phone_number=phone_number, address=address)
        db.session.add(client)
        db.session.commit()

        return redirect(url_for('show_client'))  # Assuming 'index' is your main client list view

    return render_template('create_client.html')

@app.route('/create_owner', methods=['GET', 'POST'])
def create_owner():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = str(request.form['date_of_birth'])
        phone_number = request.form['phone_number']
        address = request.form['address']

        # Create a new Owner object and add it to the database
        owner = Owner(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, phone_number=phone_number, address=address)
        db.session.add(owner)
        db.session.commit()

        return redirect(url_for('show_owner'))
    
    return render_template('create_owner.html')


@app.route('/create_agent', methods=['GET', 'POST'])
def create_agent():
    if request.method == 'POST':
        # Retrieve data from the form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = str(request.form.get('date_of_birth'))
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')

        # Create a new agent record and save it to the database
        agent = Agent(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            email=email,
            phone_number=phone_number
        )

        db.session.add(agent)
        db.session.commit()

        # Redirect to the agent list page after creating the agent
        return redirect(url_for('show_agent'))

    return render_template('create_agent.html')

@app.route('/create_contract', methods=['GET', 'POST'])
def create_contract():
    if request.method == 'POST':
        # Retrieve contract data from the form
        property_id = request.form.get('property_id')
        agent_id = request.form.get('agent_id')
        client_id = request.form.get('client_id')
        owner_id = request.form.get('owner_id')
        contract_type = request.form.get('contract_type')
        start_date = str(request.form.get('start_date'))
        end_date = str(request.form.get('end_date'))

        # Create a new contract and add it to the database
        new_contract = Contract(
            property=Property.query.get(property_id),
            agent=Agent.query.get(agent_id),
            client=Client.query.get(client_id),
            owner=Client.query.get(owner_id),
            contract_type=contract_type,
            start_date=start_date,
            end_date=end_date
        )

        db.session.add(new_contract)
        db.session.commit()

        return redirect(url_for('show_contract'))

    # If the request method is GET, render the contract creation form
    return render_template('create_contract.html')

if __name__ == '__main__':
    # Initialize the database and create tables
    #db.drop_all() # Remove this line when running the app for the first time
    #db.create_all()
    pass
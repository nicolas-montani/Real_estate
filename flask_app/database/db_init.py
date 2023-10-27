import sqlite3
from sqlite3 import Error
from db_handler import create_connection, DATABASE, add
from random_generator import *


#property(property_ID, standort, grösse, anzahl_zimmer, ausgestattet (t/f),building year)
sql_create_propertys_table = """CREATE TABLE IF NOT EXISTS propertys(
                                    id integer PRIMARY KEY,
                                    location text NOT NULL,
                                    size_m integer,
                                    rooms float,
                                    furniture boolean,
                                    building_year
                                );"""

#agents(agent_id, position, first_name, last_name, date_of_birth, email, phone_number)
sql_create_agents_table = """CREATE TABLE IF NOT EXISTS agents(
                                id integer PRIMARY KEY,
                                first_name text NOT NULL,
                                last_name text NOT NULL,
                                date_of_birth date,
                                email text NOT NULL,
                                phone_number integer
                            );"""

#client (client_id, vorname, nachname, date_of_birth, phone number, adresse)
sql_create_clients_table = """CREATE TABLE IF NOT EXISTS clients(
                                    id integer PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL,
                                    date_of_birth date,
                                    phone_number integer,
                                    address text
                                );"""
#owner(owner_id, vorname, nachname, date_of_birth, phone number, adresse)
sql_create_owners_table = """CREATE TABLE IF NOT EXISTS owners(
                                    id integer PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL,
                                    date_of_birth date,
                                    phone_number integer,
                                    address text
                                );"""

#contract (vertrag_id, immobilien_id, agent_id, client_id, owner_id, vertragsart, vertragsbeginn, vertragsende)
sql_create_contracts_table = """CREATE TABLE IF NOT EXISTS contracts(
                                    id integer PRIMARY KEY,
                                    property_id integer,
                                    agent_id integer,
                                    client_id integer,
                                    owner_id integer,
                                    contract_type text,
                                    start date NOT NULL,
                                    end date,
                                    FOREIGN KEY (property_id) REFERENCES propertys (id),
                                    FOREIGN KEY (agent_id) REFERENCES agents (id),
                                    FOREIGN KEY (client_id) REFERENCES customers (id),
                                    FOREIGN KEY (owner_id) REFERENCES owners (id)
                                );"""

#rechnungen (rechnung_id, immobilien_id, client_id, betrag, erstellt_am, fällig_am) 
sql_create_invoices_table = """CREATE TABLE IF NOT EXISTS invoices(
                                          id integer PRIMARY KEY,
                                          property_id integer,
                                          existing_credit integer,
                                          price real,
                                          created_at date NOT NULL,
                                          due_at date NOT NULL,
                                          FOREIGN KEY (property_id) REFERENCES propertys (id)
                                          );"""

#zahlungen (zahlung_id, client_id, immobilien_id, betrag, zahlungsdatum)
sql_create_payments_table = """CREATE TABLE IF NOT EXISTS payments(
                                        id integer PRIMARY KEY,
                                        invoice_id integer,
                                        client_id integer,
                                        amount real,
                                        payment_date date NOT NULL,
                                        FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                                        FOREIGN KEY (client_id) REFERENCES clients (id)
                                      );"""

#mahnungen (mahnung_id, rechnung_id, erstellt_am, fällig_datum)
sql_create_reminders_table = """CREATE TABLE IF NOT EXISTS reminders(
                                        id integer PRIMARY KEY,
                                        invoice_id integer,
                                        reminder_date date NOT NULL,
                                        due_date date NOT NULL,
                                        FOREIGN KEY (invoice_id) REFERENCES invoices (id)
                                      );"""

#meeting(agent_id, {owener_id,client_id or both}, Date, Location)
sql_create_meetings_table = """CREATE TABLE IF NOT EXISTS meetings(
                                        id integer PRIMARY KEY,
                                        agent_id integer NOT NULL,
                                        owner_id integer,
                                        client_id integer,
                                        date date,
                                        location text,
                                        FOREIGN KEY (agent_id) REFERENCES agents (id),
                                        FOREIGN KEY (owner_id) REFERENCES owners (id),
                                        FOREIGN KEY (client_id) REFERENCES clients (id)
                                      );"""



def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
    

def init_db(database):
    
    
    conn = create_connection(database)

    if conn is not None:
        # create propertys table
        print("Creating table...")
        create_table(conn, sql_create_propertys_table)
        create_table(conn, sql_create_agents_table)
        create_table(conn, sql_create_clients_table )
        create_table(conn, sql_create_owners_table )
        create_table(conn, sql_create_invoices_table)
        create_table(conn, sql_create_payments_table)
        create_table(conn, sql_create_reminders_table)
        create_table(conn, sql_create_meetings_table)

        
    else:
        print("Error! cannot create the database connection.")




def generate_properties():

    for i in range(500):
        values = str(i) + ","+ random_location() + " , " + str(random_size()) + ", " + str(random_rooms()) + ", " + str(random_bool()) + ", " + str(random_year())
        add(DATABASE, "propertys", values)
        print(values)
if __name__ == '__main__':
    #init_db(DATABASE)
    generate_properties()
    

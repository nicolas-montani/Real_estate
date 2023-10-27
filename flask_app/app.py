from flask import Flask, jsonify,request,render_template,redirect, url_for
from database.db_handler import DATABASE, search, db_add_property
import sqlite3

app = Flask(__name__)
####################################################################################################
@app.route("/")
def template():
    return render_template("index.html")

####################################################################################################

@app.route('/search-results', methods=['GET'])
def search_results():
    query = request.args.get('q')
    category = request.args.get('category')

    # Handle the search based on the selected category
    if category == 'properties':
        # Perform a search in the properties table
        results = search(DATABASE, 'propertys', query)
    elif category == 'agents':
        # Perform a search in the agents table
        results = search(DATABASE, 'agents', query)
    elif category == 'clients':
        # Perform a search in the clients table
        results = search(DATABASE, 'clients', query)
    elif category == 'owners':
        # Perform a search in the owners table
        results = search(DATABASE, 'owners', query)
    else:
        # The default category, '*' (Filter), can be used to display all results
        # If needed, you can handle this case differently
        results = []  # Empty result by default


    # Render the search results template and pass the results
    return render_template('search_results.html', results=results, query=query, category=category)

####################################################################################################
@app.route('/load-page', methods=['GET'])
def load_page():
    page = request.args.get('page')
    try:
        if page == "property.html" :
        # Render the specified HTML page
            #get all properties and tertun them to properties.html
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Retrieve all properties from the 'propertys' table
            cursor.execute("SELECT * FROM propertys")
            properties = cursor.fetchall()

            # Close the database connection
            conn.close()

            return render_template('properties.html', properties=properties)
        return render_template(page)
    except :
        return "Content not found."

#####
@app.route('/add_property', methods=['POST'])
def add_property():
    if request.method == 'POST':
        # Extract data from the form
        location = request.form['location']
        size_m = request.form['size_m']
        rooms = request.form['rooms']
        furniture = request.form['furniture']
        building_year = request.form['building_year']

        # Connect to the database
        db_add_property(location, size_m, rooms, furniture, building_year)

        # Redirect to a success page or back to the form
        return redirect(url_for('success_page'))

@app.route('/success_page')
def success_page():
    return 'Property added successfully!'

if __name__ == '__main__':
    app.run()



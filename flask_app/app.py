from flask import Flask, jsonify,request,render_template
from database.db_handler import DATABASE, search

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
        # Render the specified HTML page
        return render_template(page)
    except :
        return "Content not found."

if __name__ == '__main__':
    app.run()



from flask import Flask, jsonify,request,render_template
from database.database_handler import get_value,  set_value


app = Flask(__name__)
####################################################################################################
@app.route("/")
def template():
    return render_template("index.html")




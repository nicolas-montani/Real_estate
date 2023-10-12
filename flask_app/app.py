from flask import Flask, jsonify,request,render_template

app = Flask(__name__)
####################################################################################################
@app.route("/")
def template():
    return render_template("index.html")




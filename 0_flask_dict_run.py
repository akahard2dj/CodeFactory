from flask import Flask
from flask import render_template

import IO

app = Flask(__name__)
GoogleMaps(app)

@app.route("/json/")
def dict_test():
    json_data = IO.staticLoadJSON('960_c4List.json')
    return render_template('dict.html', parent_dict=json_data)

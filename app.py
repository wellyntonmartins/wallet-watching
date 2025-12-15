# The file that runs all the application
from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

# First route that renders when the system on
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

app.run(host='0.0.0.0', port=5000)


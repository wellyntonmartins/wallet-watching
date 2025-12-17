# The file that runs all the application
from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

# First route that renders when the system on
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)


# The file that runs all the application
from flask import Flask, request, render_template, redirect, url_for
from connection import get_db_connection
import getters, setters

app = Flask(__name__)

# First route that renders when the system on
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('home'))

# Home route thats load the main page
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

# Login route that load the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

# Authentication route that process the login authentication
@app.route('/auth', methods=['POST'])
def auth():
    email = request.form['email']
    password = request.form['password']

    #  Search the user on database
    cnx = get_db_connection()
    success, message, obj = getters.auth_login(cnx, email, password)

    # If the user exists and passwords match, redirect to home page
    if success == True:
        print("\nFrom route '/auth': User authenticated successfully!\n")
        return redirect(url_for('home'))
    else: 
        # Else if user does not exist, redirect to register page
        if obj is None: 
            print(f"\n(FAILED) From route '/auth' - {message}\n")
            return redirect(url_for('login'))
        elif obj == "UNF":
            print(f"\n(FAILED) From route '/auth' - {message}\n")
            return redirect(url_for('register'))
        # Else some error occurred during authentication
        print(f"\n(FAILED) From route '/auth' - {message}\n")
        return redirect(url_for('login'))

# Register route that load the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

# Registration route that process the user registration
@app.route('/auth_register', methods=['POST'])
def auth_register():
    email = request.form['email']
    password = request.form['repeat-password']

    # Register the user on database
    cnx = get_db_connection()
    success, message, obj = setters.auth_register(cnx, email, password)

    # If the user was registered successfully, redirect to login page
    if success == True:
        print("\nFrom route '/auth_register': User registered successfully!\n")
        return redirect(url_for('login'))
    else:
        # Else if user already exists, redirect to login page
        if obj is None:
            print(f"\n(FAILED) From route '/auth_register' - {message}\n")
            return redirect(url_for('register'))
        # Else some error occurred during registration
        else:
            print(f"\n(FAILED) From route '/auth_register' - {message}\n")
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)


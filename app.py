# The file that runs all the application
from datetime import timedelta
from flask import Flask, flash, request, render_template, redirect, session, url_for
from connection import get_db_connection
import getters, setters

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# First route that renders when the system on
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('home'))

# Home route thats load the main page
@app.route('/home', methods=['GET'])
def home():
    if 'user' not in session.keys():
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cnx = get_db_connection()
        success, message, obj = getters.auth_login(cnx, email, password)
        # If the user exists and passwords match, redirect to home page
        if success == True:
            # Store user data in session
            session['id'] = obj  
            session['user'] = email 
            print("\n(POST) From route '/login': User authenticated successfully!\n")
            flash("Authentication was a success! Welcome :)", "success")
            return redirect(url_for('home'))
        else: 
            # Else if user does not exist, redirect to register page
            if obj is None: 
                print(f"\n(POST FAILED) From route '/login' - {message}\n")
                flash("Email or password wrong. Please, try again!", "danger")
                return redirect(url_for('login'))
            elif obj == "UNF":
                print(f"\n(POST FAILED) From route '/login' - {message}\n")
                flash("This user doesn't exists on Wallet Watch. Please register!", "danger")
                return redirect(url_for('login'))
            # Else some error occurred during authentication
            print(f"\n(POST FAILED) From route '/login' - {message}\n")
            flash("Oops! Something got wrong. Please, call suport!", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')


# Register route that load the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['repeat-password']

        # Register the user on database
        cnx = get_db_connection()
        success, message, obj = setters.auth_register(cnx, email, password)  

        # If the user was registered successfully, redirect to login page
        if success == True:
            print("\nFrom route '/auth_register': User registered successfully!\n")
            flash("Authentication was a success! Welcome :)!", "danger")
            return redirect(url_for('login'))
        else:
            # Else if user already exists, redirect to login page
            if obj is None:
                print(f"\n(FAILED) From route '/auth_register' - {message}\n")
                flash("This user already exists on Wallet Watch. Please, login!", "warning")
                return redirect(url_for('register'))
            # Else some error occurred during registration
            else:
                print(f"\n(FAILED) From route '/auth_register' - {message}\n")
                flash("Oops! Something got wrong. Please, call suport!", "danger")
                return redirect(url_for('register'))
    return render_template('register.html')

# Logout route that clear the session and redirect to login page
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)


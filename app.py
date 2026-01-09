# The file that runs all the application
from datetime import timedelta, datetime
from flask import Flask, flash, request, render_template, redirect, session, url_for, jsonify, send_from_directory, Response
from connection import get_db_connection
import os
from werkzeug.utils import secure_filename
import getters, setters # Functions to set and get infos on database (MySQL)
import reports_generator

UPLOAD_FOLDER = 'static/images/payment_receipts'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Def to verify if the receipt file type is on allowed extensios
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# First route that renders when the system on
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('home'))

# Route for page "Home"
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' not in session.keys():
        return redirect(url_for('login'))
    return render_template('index.html')

# Route for page "Login"
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
                print(f"\n(FAILED POST) From route '/login' - {message}\n")
                flash("Email or password wrong. Please, try again!", "danger")
                return redirect(url_for('login'))
            elif obj == "UNF":
                print(f"\n(FAILED POST) From route '/login' - {message}\n")
                flash("This user doesn't exists on Wallet Watch. Please register!", "danger")
                return redirect(url_for('login'))
            # Else some error occurred during authentication
            print(f"\n(FAILED POST) From route '/login' - {message}\n")
            flash("Oops! Something got wrong. Please, call suport!", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

# Route for page "Register"
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['repeat-password']

        if not password == repeat_password:
            flash("Passwords doesn't match. Please, try again!", "warning")
            return redirect(url_for('register'))
        
        # Register the user on database
        cnx = get_db_connection()
        success, message, obj = setters.auth_register(cnx, email, password)  

        # If the user was registered successfully, redirect to login page
        if success == True:
            print("\nFrom route '/auth_register': User registered successfully!\n")
            flash("Authentication was a success! Welcome :)!", "success")
            return redirect(url_for('login'))
        else:
            # Else if user already exists, redirect to login page
            if obj is None:
                print(f"\n(FAILED POST) From route '/auth_register' - {message}\n")
                flash("This user already exists on Wallet Watch. Please, login!", "warning")
                return redirect(url_for('register'))
            # Else some error occurred during registration
            else:
                print(f"\n(FAILED POST) From route '/auth_register' - {message}\n")
                flash("Oops! Something got wrong. Please, call suport!", "danger")
                return redirect(url_for('register'))
    return render_template('register.html')

# Route for page "Transactions"
@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if 'user' not in session.keys():
        return redirect(url_for('login'))
    
    user_id = session['id']
    
    if request.method == 'POST':
        cnx = get_db_connection()
        success_status, message_status, status = getters.get_table_status(cnx, "transactions")
        auto_increment = 0 

        if success_status == True:
            auto_increment = int(status["Auto_increment"]) # Get 'Auto_increment' for future receipt filename if exists
        else:
            print(f"\n(FAILED WHILE GETTING TABLE STATUS) From route '/transactions' - {message_status}\n")
            flash("Oops! Something got wrong. Please, call suport!", "danger")
            return redirect(url_for('transactions'))

        # Getting requests from HTML
        transaction_type = request.form['type-select']
        category = request.form['category-select']
        fixed_cost = request.form['fixed-cost-select'] if transaction_type != 'gain' else 'N/A'
        
        unparsed_amount = request.form['amount']
        parsing_amount = unparsed_amount.replace('.', '').replace(',', '.')
        amount = float(parsing_amount)

        request_date = request.form['transaction-date'].split('-')
        transformed_date = f"{request_date[0]}/{request_date[1]}/{request_date[2]}"
        transaction_date = datetime.strptime(transformed_date, "%Y/%m/%d").date()
        
        description = request.form['description']
        file = request.files['payment-receipt']
        has_receipt = ""

        # Create receipt file on application if it has sended
        if file.filename == '':
            cnx = get_db_connection()
            has_receipt = "no"
            success, message = setters.insert_transaction(cnx, user_id, transaction_type, category, fixed_cost, amount, transaction_date, description, has_receipt)

            if success == True:
                print("\nFrom route '/transactions': Transaction successfully added !\n")
                flash(f"Transaction type '{transaction_type}' added!", "success")
                return redirect(url_for('transactions'))
            else:
                print(f"\n(FAILED POST) From route '/transactions' - {message}\n")
                flash("Oops! Something got wrong. Please, call suport!", "danger")
                return redirect(url_for('transactions'))
        else:
            if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_type = filename.rsplit(".", 1)[1].lower()
                    has_receipt = "yes"

                    try:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{auto_increment}.{file_type}"))
                        cnx = get_db_connection()
                        success, message = setters.insert_transaction(cnx, user_id, transaction_type, category, fixed_cost, amount, transaction_date, description, has_receipt)

                        if success == True:
                            print("\nFrom route '/transactions': Transaction successfully added !\n")
                            flash(f"Transaction type '{transaction_type}' added! (with payment receipt)", "success")
                            return redirect(url_for('transactions'))
                        else:
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            print(f"\n(FAILED POST) From route '/transactions' - {message}\n")
                            flash("Oops! Something got wrong. Please, call suport!", "danger")
                            return redirect(url_for('transactions'))
                    except Exception as e:
                        print(f"\n(FAILED POST) From route '/transactions'- Failed to save file: {e} \n")
                        flash("Oops! Something got wrong. Please, call suport!", "danger")
                        return redirect(url_for('transactions'))
            else:
                print(f"\n(FAILED POST) From route '/transactions'- Not allowed filename \n")
                flash("Oops! Something got wrong. Please, call suport!", "danger")
                return redirect(url_for('transactions'))
    # If method is 'GET'
    cnx = get_db_connection()
    success, message, transactions = getters.get_transactions(cnx, user_id)

    # To store the values for overview
    total_expenses = 0
    total_gains = 0
    total_in_account = 0

    expenses_list = {
        'tax': 0,
        'food': 0,
        'transport': 0,
        'leisure': 0,
        'shopping': 0,
        'studies': 0,
        'health': 0,
        'transfer': 0,
        'emergency': 0,
        'other': 0,
    } 

    gains_list = {
        'salary': 0,
        'extra_income': 0,
        'capital_gain': 0,
        'transfer': 0,
        'other': 0,
    } 

    # Count for each type of transactions (To future chart.js)
    count_expenses = 0
    count_gains = 0

    if success == True:
        for transaction in transactions:
            # Seting the values... 
            if transaction["type"] == "expense":
                total_expenses += transaction["amount"]

                if transaction["category"] in expenses_list:
                    category = transaction["category"] 
                    expenses_list[category] += 1
            else:
                total_gains += transaction["amount"]

                if transaction["category"] in gains_list:
                    category = transaction["category"] 
                    gains_list[category] += 1
        
        total_in_account = total_gains - total_expenses

        # Seting the count values...
        for category_count in expenses_list: 
            if expenses_list[f'{category_count}'] > 0:
                count_expenses += 1

        for category_count in gains_list:
            if gains_list[f'{category_count}'] > 0:
                count_gains += 1

        # Sorting listis...
        if count_expenses == 0:
            sorted_expenses_list = None
        else:
            sorted_expenses_list = dict(sorted(expenses_list.items(), key=lambda item: item[1], reverse=True))
        
        if count_gains == 0:
            sorted_gains_list = None    
        else:
            sorted_gains_list = dict(sorted(gains_list.items(), key=lambda item: item[1], reverse=True))


        print("\nFrom route '/transactions': Transactions successfully redeemed !\n")
        return render_template('transactions.html', transactions=transactions, total_gains=total_gains, total_expenses=total_expenses, total_in_account=total_in_account, expenses_list=sorted_expenses_list, gains_list=sorted_gains_list)
    else:
        print(f"\n(FAILED GET) From route '/transactions' - {message}\n")
        flash("Oops! Something got wrong. Please, call suport!", "danger")
        return redirect(url_for('transactions'))

# Route for page "Reports"
@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if 'user' in session:
        return render_template("reports.html")
    else:
        return redirect(url_for('login'))

# Route to generate the requested report
@app.route('/generate_report', methods=['GET']) 
def generate_report():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_id = session['id']
    email = session['user']
    
    # Generating PDF...
    pdf_bytes = reports_generator.generate_monthly_report(user_id, email)
    
    if pdf_bytes:
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=monthly_report.pdf'})
    else:
        flash("Error generating report", "danger")
        return redirect(url_for('reports'))

# Route for page "Wish List"
@app.route('/wishlist', methods=['GET', 'POST', 'UPDATE', 'DELETE'])
def wishlist():
    if 'user' in session:
        user_id = session['id']
        
        if request.method == 'POST':
            wish = request.form["wish"]

            cnx = get_db_connection()

            success, message = setters.insert_wish(cnx, user_id, wish)

            if success == True:
                print("\n(POST) From route '/wishlist': Wish successfully added !\n")
                flash(f"Wish added!", "success")
                return redirect(url_for('wishlist'))
            else:
                print(f"\n(FAILED POST) From route '/wishlist' - {message}\n")
                flash("Oops! Something got wrong. Please, call suport!", "danger")
                return redirect(url_for('wishlist'))
        elif request.method == 'UPDATE':
            data = request.get_json()
            wish_id = data.get("wish_id")
            its_done_get = data.get("its_done")

            print(f"\nIts done get: {its_done_get}")
            its_done = ""

            if its_done_get:
                its_done = "yes"
            else:
                its_done = "no"

            print(f"\nIts done: {its_done_get}")
            cnx = get_db_connection()

            success, message = setters.update_wish(cnx, wish_id, its_done)

            if success == True:
                print("\n(UPDATE) From route '/wishlist': Wish Successfully Updated !\n")
                flash(f"Wish successfully updated!", "success")
                return jsonify({'success': True})
            else:
                print(f"\n(FAILED UPDATE) From route '/wishlist' - {message}\n")
                flash("Oops! Something got wrong. Please, call suport!", "danger")
                return jsonify({'success': False})
        elif request.method == 'DELETE':
            data = request.get_json()
            wish_id = data.get("wish_id")

            cnx = get_db_connection()

            success, message = setters.delete_wish(cnx, wish_id)

            if success == True:
                print("\n(DELETE) From route '/wishlist': Wish Successfully Deleted !\n")
                flash(f"Wish successfully deleted!", "success")
                return jsonify({'success': True})
            else:
                print(f"\n(FAILED DELETE) From route '/wishlist' - {message}\n")
                flash("Oops! Something got wrong. Please, call suport!", "danger")
                return jsonify({'success': False})
        else:
            cnx = get_db_connection()

            success, message, wishlist = getters.get_wishlist(cnx, user_id)

            if success == True:
                print("\n(GET) From route '/wishlist': Wishes Successfully Loaded !\n")
                return render_template("wishlist.html", wishlist=wishlist)
            else:
                print(f"\n(FAILED GET) From route '/wishlist' - {message}\n")
                flash("Oops! Something got wrong. Please, call suport!", "danger")
                return render_template("wishlist.html", wishlist=None)
    else:
        return redirect(url_for('login'))

# Route to download the requested receipt
@app.route('/download_receipt/<int:receipt_id>', methods=['GET'])
def download_receipt(receipt_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    directory = app.config['UPLOAD_FOLDER']
    abs_directory = os.path.abspath(directory) 
    
    for filename in os.listdir(abs_directory):
        base_name, ext = os.path.splitext(filename)
        if base_name == str(receipt_id) and ext[1:].lower() in ALLOWED_EXTENSIONS:
            try:
                download_name = f"RECEIPT_{receipt_id}{ext}"
                print(f"\n(GET) From route '/download_receipt': Sending file {filename} as {download_name}")
                flash("Payment receipt downloaded successfully!", "success")

                return send_from_directory(
                    directory,
                    filename,
                    as_attachment=True,
                    download_name=download_name,
                    mimetype='application/octet-stream'  
                )
            except Exception as e:
                print(f"\n(FAILED GET) From route '/download_receipt': {e}")
                flash("Oops! Something got wrong. Please, call support!", "danger")
                return redirect(url_for('transactions'))
    
    print(f"\n(FAILED GET) From route '/download_receipt': File not found for ID {receipt_id}")
    flash("Receipt not found. Please, call support!", "danger")
    return redirect(url_for('transactions'))



# Logout route that clear the session and redirect to login page
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


import hashlib

def auth_login(cnx, email, password):
    cursor = None

    try:
        encrypted_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        cursor = cnx.cursor(dictionary=True)

        check_email_query = "SELECT * FROM user WHERE email = %s"
        cursor.execute(check_email_query, (email,))
        existing_user = cursor.fetchone()

        if not existing_user:
            return False, "User is not registered. Please register first or try another account!", "UNF"
        
        query = "SELECT * FROM user WHERE email = %s AND password = %s"
        cursor.execute(query, (email, encrypted_password))
        result = cursor.fetchone() 

        if result:
            return True, "The credentials are valid.", result['id']
        else:
            return False, "Email or password is incorrect. Please try again!", None
    except Exception as e:
        return False, f"Error during authentication: {e}", "Exception"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

def get_transactions(cnx, user_id):
    cursor = None

    try:
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM transactions WHERE user_id = %s ORDER BY transaction_date DESC"
        cursor.execute(query, (user_id,))
        transactions = cursor.fetchall() 

        return True, "User transactions successfully redeemed", transactions
    except Exception as e:
        return False, f"Error during get user transactions: {e}", "Exception"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

def get_wishlist(cnx, user_id):
    cursor = None

    try:
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM wishlist WHERE user_id = %s ORDER BY id DESC"
        cursor.execute(query, (user_id,))
        wishlist = cursor.fetchall() 

        return True, "User wishlist successfully redeemed", wishlist
    except Exception as e:
        return False, f"Error during get user wishlist: {e}", "Exception"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

def get_table_status(cnx, table):
    cursor = None

    try:
        cursor = cnx.cursor(dictionary=True)

        query = "SHOW TABLE STATUS LIKE %s"
        cursor.execute(query, (table,))
        status = cursor.fetchone() 

        return True, "Table status successfully redeemed", status
    except Exception as e:
        return False, f"Error during get table status: {e}", "Exception"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
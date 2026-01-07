# Authentication Registration 
def auth_register(cnx, email, password):
    cursor = None

    try:
        cursor = cnx.cursor(dictionary=True)

        check_email_query = "SELECT * FROM user WHERE email = %s"
        cursor.execute(check_email_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return False, "Email already registered. Please use a different email or login", None

        query = "INSERT INTO user (email, password) VALUES (%s, md5(%s))"
        cursor = cnx.cursor()
        cursor.execute(query, (email, password))
        cnx.commit()

        return True, "User registered successfully", None
    except Exception as e:
        cnx.rollback()
        return False, f"Error during registration: {e}", "Exception"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

def insert_transaction(cnx, user_id, transaction_type, category, fixed_cost, amount, date, description, has_receipt):
    cursor = None

    try:
        cursor = cnx.cursor(dictionary=True)

        query = "INSERT INTO transactions (user_id, type, category, fixed_cost, amount, transaction_date, description, has_receipt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (user_id, transaction_type, category, fixed_cost, amount, date, description, has_receipt, ))
        cnx.commit()

        return True, "Transaction successfully added"
    except Exception as e:
        cnx.rollback()
        return False, f"Error during transaction add: {e}"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

def insert_wish(cnx, user_id, wish_name):
    cursor = None

    try:
        cursor = cnx.cursor(dictionary=True)

        query = "INSERT INTO wishlist (user_id, wish_name, its_done) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, wish_name, 'no',))
        cnx.commit()

        return True, "Wish successfully added"
    except Exception as e:
        cnx.rollback()
        return False, f"Error during wish add: {e}"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

def update_wish(cnx, wish_id, its_done):
    cursor = None

    try:
        cursor = cnx.cursor(dictionary=True)

        query = "UPDATE wishlist SET its_done = %s WHERE id = %s"
        cursor.execute(query, (its_done, wish_id,))
        cnx.commit()

        return True, "Wish successfully updated"
    except Exception as e:
        cnx.rollback()
        return False, f"Error during wish update: {e}"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

def delete_wish(cnx, wish_id):
    cursor = None

    try:
        cursor = cnx.cursor(dictionary=True)

        query = "DELETE FROM wishlist WHERE id = %s"
        cursor.execute(query, (wish_id,))
        cnx.commit()

        return True, "Wish successfully deleted"
    except Exception as e:
        cnx.rollback()
        return False, f"Error during wish update: {e}"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
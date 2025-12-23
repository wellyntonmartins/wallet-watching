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
            return True, "The credentials are valid.", None
        else:
            return False, "Email or password is incorrect. Please try again!", None
    except Exception as e:
        return False, f"Error during authentication: {e}", "Exception"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

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
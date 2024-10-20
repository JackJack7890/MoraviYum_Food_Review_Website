import dotenv
import os
import uuid
import mysql.connector
import pathlib
import requests
import google.auth.transport.requests
import pip._vendor.cachecontrol as cachecontrol
import time
import redis
from authlib.integrations.flask_client import OAuth
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from functools import wraps
from flask import Flask, abort, jsonify, redirect, request, session, render_template, url_for
from flask_session import Session

dotenv.load_dotenv
if not os.getenv('FLASK_SECRET_KEY'):
    print('Please set FLASK_SECRET_KEY in .env file')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# OAUTH CONFIG
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri = "https://www.googleapis.com/oauth2/v3/certs",
    clock_skew_in_seconds=10
)

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'email' not in session:  # Check if the user is logged in
            return abort(401)  # If not, return 401 Unauthorized
        else:
            return function(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/moravian_star.png', methods=['GET'])
def moravian_star():
    return app.send_static_file('moravian_star.png')

@app.route('/user_profile.png', methods=['GET'])
def user_profile():
    return app.send_static_file('user_profile.png')

@app.route('/review')
@login_is_required # Decorator to check if the user is logged in
def review():
    email = session.get('email').strip()
    user_handle = get_user_handle(email)
    return render_template('review.html', user_handle=user_handle)

def get_user_handle(email):
    cursor, connection = connectToMySQL()

    use_db = f"USE {os.getenv('MYSQL_DATABASE')}"
    cursor.execute(use_db)
    cursor.execute("SELECT user_handle FROM usernames WHERE email = %s", (email,))
    user_handle = cursor.fetchone()

    cursor.close()
    connection.close()

    if user_handle is None:
        # Handle case where no user_handle is found for the email
        print(f"No user_handle found for email: {email}")
        abort(404)  # Optionally return a 404 error or handle it differently
    else:
        return user_handle[0]

@app.route('/new_user')
@login_is_required # Decorator to check if the user is logged in
def new_user():
    user_name = session.get('name')
    print("we have reached this point SUCCESSFULLY")
    return render_template('new_user.html', user_name=user_name)

@app.route('/store_user_handle', methods=['POST'])
def store_user_handle():
    user_handle = request.get_json()
    user_handle = user_handle['user_handle']
    cursor, connection = connectToMySQL()

    use_db = f"USE {os.getenv('MYSQL_DATABASE')}"
    cursor.execute(use_db)

    cursor.execute("INSERT INTO usernames (email, user_handle) VALUES (%s, %s)", (session['email'], user_handle))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User handle saved successfully!'}), 200



@app.route('/login')
def login():
    google = oauth.create_client('google') # Create/get the google client above
    redirect_uri = url_for('authorize', _external=True)
    session.pop('is_faculty', None) # Remove the faculty flag if it exists since this is regular student login
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/logout') 
def logout():
    for key in list(session.keys()): # Clear all keys from the session data
        session.pop(key)
    return redirect('/')

@app.route('/authorize')
def authorize():
   
    google = oauth.create_client('google') # Create/get the google client above
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo')
    user_info = resp.json()
    # Store the user's email, google_id, and name in the session
    session['email'] = user_info['email']
    session['name'] = user_info['name']
    session['google_id'] = user_info['id']

    cursor, cnx = connectToMySQL()

    try:
        use_db = os.getenv('MYSQL_DATABASE')
        cursor.execute(f"USE {use_db}")
        # Check if user already exists in the session table
        query_check = "SELECT * FROM session WHERE email = %s"
        cursor.execute(query_check, (session['email'],))
        existing_user = cursor.fetchone()  # Fetch the first row

        if existing_user:
            # Updates the existing user if necessary
            query_update = "UPDATE session SET username = %s WHERE email = %s"
            cursor.execute(query_update, (session['name'], session['email']))
            cnx.commit()
            session.pop('is_new_user', None)
        else:
            # Insert the new user if they do not exist in the session table
            query_insert = "INSERT INTO session (user_id, username, email) VALUES (%s, %s, %s)"
            cursor.execute(query_insert, (session['google_id'], session['name'], session['email']))
            cnx.commit()
            session['is_new_user'] = True
          

    except mysql.connector.Error as err:
        print(f"Error during login: {err}")
        cnx.rollback()  # Rollback the transaction in case of error
        return abort(500)

    finally:
        cursor.close()
        cnx.close()

    # Redirect based on the user type (faculty or student)
    if session.get('is_new_user'):
        return redirect('/new_user')
    else:
        return redirect('/review')
    
def connectToMySQL():
    '''
    Connects to MySQL and returns a cursor and connection object.
    '''
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DB = os.getenv('MYSQL_DB')

    cnx = mysql.connector.connect(user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DB)
    #Tried with user = root, password = password, host = most recent AWS ip
    cursor = cnx.cursor()
    return cursor, cnx

if __name__ == '__main__':
    app.run(debug=True, port=8000, host="0.0.0.0")
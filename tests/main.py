from flask import Flask, render_template, request, redirect, url_for, session
import re
import mysql.connector

app = Flask(__name__)

app.secret_key = 'buildsdg'

db_check= mysql.connector.connect(user='root', password='', db='yemp')
cursor = db_check.cursor()

# http://localhost:5000/yemp/login - this will be the login page, we need to use both GET and POST requests
@app.route('/yemp/login', methods=['GET', 'POST'])
def login():
        # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        query = ("SELECT * FROM youth_profile " "WHERE email LIKE %s" "AND password LIKE %s")
        
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        #print(result[0][2])
                # If result exists in profile table in our database
        if result:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['surname'] = result[0][0]
            session['email'] = result[0][2]
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Invalid email/password!'

    return render_template('index.html', msg=msg)

# http://localhost:5000/yemp/logout - this will be the logout page
@app.route('/yemp/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('surname', None)
    session.pop('email', None)
   # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/yemp/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/yemp/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'surname' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        surname = request.form['surname']
        query = ("SELECT * FROM youth_profile " 
                "WHERE email LIKE %s")
        
        cursor.execute(query, (email,))
        result1 = cursor.fetchone()
        # If account exists show error and validation checks
        if result1:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            query = "INSERT INTO youth_profile (email,password,surname) " \
                    "VALUES (%s,%s,%s)"
                    
            cursor.execute(query, (email,password,surname))
            db_check.commit()
            #cursor.close()
            #db_check.close() 
            msg = 'You have successfully registered!'
        
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
           
    return render_template('register.html', msg=msg)

# http://localhost:5000/yemp/home - this will be the home page, only accessible for loggedin users
@app.route('/yemp/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', surname=session['surname'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/yemp/profile - this will be the profile page, only accessible for loggedin users
@app.route('/yemp/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        
        query = ("SELECT * FROM youth_profile " "WHERE email LIKE %s")
        
        cursor.execute(query, (session['email'],))
        result = cursor.fetchone()
        
        # Show the profile page with account info
        return render_template('profile.html', account=result)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
app.run(debug=True, port=5000)

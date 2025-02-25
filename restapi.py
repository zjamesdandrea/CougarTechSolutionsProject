import flask

from flask import jsonify
from flask import request

from sql import DBconnection
from sql import execute_read_query
from sql import execute_update_query

import creds
import smtplib

#setup an application
app = flask.Flask(__name__)
app.config['DEBUG'] = True

#-------------------User CRUD------------------------
# Return all users (admin)
@app.route('/user/all', methods = ['GET'])
def all_user():
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = "select * from Users"

    userrows = execute_read_query(mycon, sql)
    return jsonify(userrows)

# Return user by ID (admin)
@app.route("/user/", methods=['GET'])
def select_user():
    user_id = request.args.get('id')
    if not user_id:
        return 'Error: No ID provided'
    
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"select * from Users where id = {user_id}"
    userrows = execute_read_query(mycon, sql)
    return jsonify(userrows)

# Register user (customer)
@app.route("/user", methods=['POST'])
def add_user():
    data = request.get_json()
    fname = data['first_name']
    lname = data['last_name']
    email = data['email']
    password = data['password']
    address = data['address']
    city = data['city']
    state = data['state']
    zip_code = data['zip']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"INSERT INTO Users (first_name, last_name, email, password, address, city, state, zip) VALUES ('{fname}', '{lname}', '{email}', '{password}', '{address}', '{city}', '{state}', '{zip_code}')"
    
    execute_update_query(mycon, sql)
    return "User registration successful"

# Update user info by ID (customer)
@app.route("/user", methods=['PUT'])
def update_user():
    data = request.get_json()
    user_id = data['id']
    email = data['email']
    address = data['address']
    city = data['city']
    state = data['state']
    zip = data['zip']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"UPDATE Users SET email = '{email}', address = '{address}', city = '{city}', state = '{state}', zip = '{zip}' WHERE id = '{user_id}'"
    execute_update_query(mycon, sql)
    return "User information update successful"





app.run()
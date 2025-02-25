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
# Register a new customer
@app.route("/user", methods=['POST'])
def register_user():
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
    
    sql = f"INSERT INTO user (first_name, last_name, email, password, address, city, state, zip) VALUES ('{fname}', '{lname}', '{email}', '{password}', '{address}', '{city}', '{state}', '{zip_code}')"
    execute_update_query(mycon, sql)
    
    return "User registration successful"

# Update customer information
@app.route("/user", methods=['PUT'])
def update_user():
    data = request.get_json()
    id = data['id']
    email = data['email']
    address = data['address']
    city = data['city']
    state = data['state']
    zip_code = data['zip']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    sql = f"UPDATE user SET email = '{email}', address = '{address}', city = '{city}', state = '{state}', zip = '{zip_code}' WHERE id = '{id}'"
    execute_update_query(mycon, sql)
    
    return "User update successful"

# Delete a user account
@app.route("/user", methods=['DELETE'])
def delete_user():
    data = request.get_json()
    id = data['id']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    sql = f"DELETE FROM user WHERE id = '{id}'"
    execute_update_query(mycon, sql)
    
    return "User deleted successfully"



app.run()
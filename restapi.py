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

# Delelte user by ID (customer)
@app.route('/user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    idtodelete = data['id']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"delete from Users where id = '{idtodelete}'"
    execute_update_query(mycon, sql)
    return "User deletion successful"

#---------------------Card CRUD----------------------------
# Retun all baseball cards (customer/admin)
@app.route('/card/all', methods = ['GET'])
def all_card():
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = "select * from Baseball_Cards"

    userrows = execute_read_query(mycon, sql)
    return jsonify(userrows)

# Select card by ID (customer/admin)
@app.route("/card/", methods=['GET'])
def select_card():
    card_id = request.args.get('id')
    if not card_id:
        return 'Error: No ID provided'
    
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"select * from Baseball_Cards where id = {card_id}"
    userrows = execute_read_query(mycon, sql)
    return jsonify(userrows)

# Add new card (admin)
@app.route("/card", methods=["POST"])
def add_card():
    data = request.get_json()
    fname = data['first_name']
    lname = data['last_name']
    team = data['team']
    autograph = data['autograph']
    price = data['price']
    image_url = data['image_url']
    additional_specification = data['additional_specifications']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"INSERT INTO Baseball_Cards (first_name, last_name, team, autograph, price, image_url, additional_specifications) VALUES ('{fname}', '{lname}', '{team}', '{autograph}', '{price}', '{image_url}', '{additional_specification}')"
    execute_update_query(mycon, sql)
    return "Baseball card added successfully"

# Update card information by ID (admin)
@app.route("/card", methods=["PUT"])
def update_card():
    data = request.get_json()
    card_id = data['id']
    team = data['team']
    autograph = data['autograph']
    price = data['price']
    image_url = data['image_url']
    additional_specifications = data['additional_specifications']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"UPDATE Baseball_Cards SET team = '{team}', autograph = '{autograph}', price = '{price}', image_url = '{image_url}', additional_specifications = '{additional_specifications}' WHERE id = '{card_id}'"
    execute_update_query(mycon, sql)
    return "Baseball card updated successfully"

# Delete card by ID (admin)
@app.route('/card', methods=['DELETE'])
def delete_card():
    data = request.get_json()
    idtodelete = data['id']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"delete from Baseball_Cards where id = '{idtodelete}'"
    execute_update_query(mycon, sql)
    return "Baseball card deletion successful"



app.run()
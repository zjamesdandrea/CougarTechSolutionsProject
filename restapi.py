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

#-------------------Cart CRUD------------------------------
# Retun all cart (admin)
@app.route("/cart/all", methods=['GET'])
def all_carts():
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    sql = """
        SELECT c.id AS cart_id, c.user_id, u.first_name, u.last_name, 
               b.id AS card_id, b.first_name AS card_firstname, 
               b.last_name AS card_lastname, b.team, b.autograph, 
               b.price, b.image_url, b.additional_specifications
        FROM Cart c
        JOIN Users u ON c.user_id = u.id
        JOIN Baseball_Cards b ON c.card_id = b.id
    """

    cart_rows = execute_read_query(mycon, sql)
    return jsonify(cart_rows)


# Select cart by User_ID (customer)
@app.route("/cart/", methods=['GET'])
def select_cart():
    user_id = request.args.get('user_id')
    if not user_id:
        return 'Error: No User ID provided'
    
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"""
        SELECT c.id AS cart_id, c.user_id, u.first_name, u.last_name, 
               b.id AS card_id, b.first_name AS card_firstname, 
               b.last_name AS card_lastname, b.team, b.autograph, 
               b.price, b.image_url, b.additional_specifications
        FROM Cart c
        JOIN Users u ON c.user_id = u.id
        JOIN Baseball_Cards b ON c.card_id = b.id
        WHERE c.user_id = {user_id}
    """

    cart_rows = execute_read_query(mycon, sql)
    return jsonify(cart_rows)

# Add cards to cart (customer)
@app.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    cart_ids = data.get('cart_ids')  # List of card IDs

    if not user_id or not cart_ids:
        return jsonify({"error": "User ID and cart IDs are required"}), 400

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    values = ", ".join(f"({user_id}, {card_id})" for card_id in cart_ids)
    sql = f"INSERT INTO Cart (user_id, cart_id) VALUES {values}"
    execute_update_query(mycon, sql)
    return jsonify({"message": f"{len(cart_ids)} baseball cards added to cart successfully"})




app.run()
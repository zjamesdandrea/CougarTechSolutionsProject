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

#------------------Hardcode admin credential--------------------
admin_username = "admin"
admin_password = "password"

def is_admin(auth):
    return auth and auth.get("username") == admin_username and auth.get("password") == admin_password

#-------------------User CRUD------------------------
# Return all users (admin)
@app.route('/user/all', methods = ['GET'])
def all_user():
    auth = request.get_json()
    if not is_admin(auth):
        return "Error: Unauthorized"

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
    additional_specifications = data['additional_specifications']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"INSERT INTO Baseball_Cards (first_name, last_name, team, autograph, price, image_url, additional_specifications) VALUES ('{fname}', '{lname}', '{team}', '{autograph}', '{price}', '{image_url}', '{additional_specifications}')"
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
# Create a cart for a user (customer)
@app.route('/cart', methods=['POST'])
def create_cart():
    data = request.get_json()
    user_id = data['user_id']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    
    sql = f"INSERT INTO Cart (user_id) VALUES ('{user_id}')"
    execute_update_query(mycon, sql)

    return "Cart created successfully"

# Retrieve a user's cart with items (customer)
@app.route('/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('user_id')
    if not user_id:
        return 'Error: No user ID provided'
    
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    sql = f"""
        SELECT ci.id AS cart_item_id, ci.cart_id, ci.baseball_card_id, ci.quantity,
               b.first_name, b.last_name, b.team, b.autograph, b.price, b.image_url
        FROM Cart_Items ci
        JOIN Cart c ON ci.cart_id = c.id
        JOIN Baseball_Cards b ON ci.baseball_card_id = b.id
        WHERE c.user_id = {user_id}
    """
    
    cart_items = execute_read_query(mycon, sql)
    return jsonify(cart_items)

# Add a baseball card to a user's cart (customer)
@app.route('/cart/item', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    cart_id = data['cart_id']
    baseball_card_id = data['baseball_card_id']
    quantity = data.get('quantity', 1)

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    
    sql = f"""
        INSERT INTO Cart_Items (cart_id, baseball_card_id, quantity)
        VALUES ('{cart_id}', '{baseball_card_id}', '{quantity}')
    """
    execute_update_query(mycon, sql)
    
    return "Baseball card added to cart successfully"

# Update item quantity in cart (customer)
@app.route('/cart/item', methods=['PUT'])
def update_cart_item():
    data = request.get_json()
    cart_item_id = data['cart_item_id']
    quantity = data['quantity']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    
    sql = f"UPDATE Cart_Items SET quantity = '{quantity}' WHERE id = '{cart_item_id}'"
    execute_update_query(mycon, sql)

    return "Cart item updated successfully"

# Remove an item from the cart (customer)
@app.route('/cart/item', methods=['DELETE'])
def remove_cart_item():
    data = request.get_json()
    cart_item_id = data['cart_item_id']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    
    sql = f"DELETE FROM Cart_Items WHERE id = '{cart_item_id}'"
    execute_update_query(mycon, sql)

    return "Cart item removed successfully"

# Delete a user's entire cart (customer)
@app.route('/cart', methods=['DELETE'])
def delete_cart():
    data = request.get_json()
    cart_id = data['cart_id']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    sql = f"DELETE FROM Cart WHERE id = '{cart_id}'"
    execute_update_query(mycon, sql)

    return "Cart deleted successfully"

#---------------Interest Form (checkout)-----------------------------




app.run()
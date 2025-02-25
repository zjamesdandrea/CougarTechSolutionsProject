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

# ------------------- User CRUD ------------------------
# Register a new customer
@app.route("/user", methods=['POST'])
def register_user():
    data = request.get_json()
    fname, lname = data['first_name'], data['last_name']
    email, password = data['email'], data['password']
    address, city, state, zip_code = data['address'], data['city'], data['state'], data['zip']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    
    sql = "INSERT INTO user (first_name, last_name, email, password, address, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (fname, lname, email, password, address, city, state, zip_code)

    execute_update_query(mycon, sql, values)
    mycon.close()
    
    return jsonify({"message": "User registration successful"}), 201

# Update customer information
@app.route("/user", methods=['PUT'])
def update_user():
    data = request.get_json()
    user_id, email = data['id'], data['email']
    address, city, state, zip_code = data['address'], data['city'], data['state'], data['zip']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    sql = "UPDATE user SET email = %s, address = %s, city = %s, state = %s, zip = %s WHERE id = %s"
    values = (email, address, city, state, zip_code, user_id)

    execute_update_query(mycon, sql, values)
    mycon.close()
    
    return jsonify({"message": "User update successful"}), 200

# Delete a user account
@app.route("/user", methods=['DELETE'])
def delete_user():
    data = request.get_json()
    user_id = data['id']

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    # Check if user exists before deleting
    check_sql = "SELECT id FROM user WHERE id = %s"
    if not execute_read_query(mycon, check_sql, (user_id,)):
        return jsonify({"error": "User not found"}), 404

    sql = "DELETE FROM user WHERE id = %s"
    execute_update_query(mycon, sql, (user_id,))
    mycon.close()
    
    return jsonify({"message": "User deleted successfully"}), 200

# Get all users (admin)
@app.route("/user/all", methods=['GET'])
def get_all_users():
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    sql = "SELECT id, first_name, last_name, email, address, city, state, zip FROM user"
    users = execute_read_query(mycon, sql)

    mycon.close()
    return jsonify(users), 200

# Get user by ID
@app.route("/user/<int:id>", methods=['GET'])
def get_user_by_id(id):
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    sql = "SELECT id, first_name, last_name, email, address, city, state, zip FROM user WHERE id = %s"
    user = execute_read_query(mycon, sql, (id,))

    mycon.close()

    if user:
        return jsonify(user[0]), 200  # Return the first matching record
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run()
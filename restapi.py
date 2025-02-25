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
    sql = "select * from user"

    userrows = execute_read_query(mycon, sql)
    return jsonify(userrows)

# Return user by ID (admin)
@app.route("/user", methods=['GET'])
def select_user():
    user_id = id = request.args.get('id')
    if not user_id:
        return 'Error: No ID provided'
    
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"select * from investor where id = {user_id}"
    userrows = execute_read_query(mycon, sql)
    return jsonify(userrows)

# Register user (customer)


app.run()
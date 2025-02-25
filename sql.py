import mysql.connector
from mysql.connector import Error

def DBconnection(hostname, uname, pwd, dbname):
    con = None
    try:
        con = mysql.connector.connect(
            host = hostname,
            user = uname,
            password = pwd,
            database = dbname
        )
        print("Connection successful")
    except Error as e:
        print("Connection unsuccessful due to Error ", e)
    return con

# Execute query function to read rows from table
def execute_read_query(con, sql):
    mycursor = con.cursor(dictionary=True)
    rows = None
    try:
        mycursor.execute(sql)
        rows = mycursor.fetchall()
        return rows
    except Error as e:
        print("Error is: ", e)

# Execute query function to insert the rows into the table
def execute_update_query(con, sql):
    mycursor = con.cursor()
    try:
        mycursor.execute(sql)
        con.commit()
        print("DB update is successful")
    except Error as e:
        print('Error is: ', e)

# If script is being executed directly, test the DB connection
if __name__ == "__main__":
    from creds import myCreds  # Import your credentials class
    mycreds = myCreds()
    con = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    
    if con:
        print("Connection test successful")
    else:
        print("Failed to connect")

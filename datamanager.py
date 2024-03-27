import sqlite3 as sql
import hashlib as hl

class Data_Manager():
    def connectToDatabase():
        connection = sql.connect("Data/local_database.db")
        cur = connection.cursor()
        return(connection, cur)
    
    def createDatabase(connection, cur):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS userdata (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
        )            
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS usersettings (
                    id INTEGER PRIMARY KEY,
                    apperancemode BOOL,
                    colortheme VARCHAR(10),
                    FOREIGN KEY (id) REFERENCES userdata (id)
        )
        """)
        #type: IP, Port, Protocol. WHitlisttype: white or black. 
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Whitelists (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(16) NOT NULL,
                    whitelisttype BOOL NOT NULL
        )
        """)
        connection.commit()

    def insertUser(connection, cur, username, password):
        encrypted_pass = hl.sha256(password.encode()).hexdigest()
        try:
            cur.execute("""
            INSERT INTO userdata (user, pass) VALUES (?,? )           
            """, (username, encrypted_pass))
            connection.commit()
        except:
            sql.IntegrityError()
            return("Unique Username is Required")

    def findPassword(connection, cur, username):
        print(username)
        cur.execute("SELECT * FROM userdata")
        print(cur.fetchall())
        cur.execute("SELECT password FROM userdata WHERE username IS ?", (username,))
        return(cur.fetchall())
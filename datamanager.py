import sqlite3 as sql
import hashlib as hl
import json

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
        #type: IP, Port, Protocol. WHitlisttype: white or black. 
        cur.execute("""
        CREATE TABLE IF NOT EXISTS whitelists (
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(16) NOT NULL,
                    whitelisttype BOOL NOT NULL,
                    PRIMARY KEY (name, type)
        )
        """)
        connection.commit()

    def insertUser(connection, cur, username, password):
        encrypted_pass = Data_Manager.encryptPassword(password)
        try:
            cur.execute("""
            INSERT INTO userdata (username, password) VALUES (?,?)           
            """, (username, encrypted_pass))
            connection.commit()
        except:
            sql.IntegrityError()
            return("Unique Username is Required")
        
    def encryptPassword(password):
        return hl.sha256(password.encode()).hexdigest()

    def findPassword(connection, cur, username):
        cur.execute("SELECT * FROM userdata")
        cur.execute("SELECT password FROM userdata WHERE username IS ?", (username,))
        return(cur.fetchall())
    
    def open_theme(theme):
        file = open("Data/Themes/"+theme+".json")
        theme = json.load(file)
        file.close()
        return theme
    
    def read_settings():
        file = open("Data/settings.json")
        settings = json.load(file)
        file.close
        return settings
    
    def update_setting(setting, new_value):
        file = open("Data/settings.json", "r+")
        settings = json.load(file)
        settings[setting] = new_value
        file.seek(0)
        json.dump(settings, file, indent=4)
        file.truncate()
        file.close

    def remove_rule(type, target, iswhitelisted, cur, connection):
        print("Removing Rule" + type + " " + target + " " + iswhitelisted)
        cur.execute("""
            DELETE FROM whitelists WHERE name=? AND type=? AND whitelisttype=?           
            """, (target, type, iswhitelisted))
        connection.commit()
        print("Rule " + type + " " + target + " " + iswhitelisted+" removed")
        

    def add_rule(type, target, iswhitelisted, cur, connection):
        print("Adding Rule" + type + " " + target + " " + iswhitelisted)
        try:
            cur.execute("""
                INSERT INTO whitelists (name, type, whitelisttype) VALUES (?, ?, ?)           
                """, (target, type, iswhitelisted))
            connection.commit()
            print("Rule " + type + " " + target + " " + iswhitelisted+" Added")
            return("Added")
        except:
            sql.IntegrityError()
            return("Unique Rule is Required")
        
    def fetch_rules(cur, type):
        cur.execute("SELECT * FROM whitelists WHERE type IS ?", (type,))
        return cur.fetchall()
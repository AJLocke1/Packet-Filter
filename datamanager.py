import sqlite3 as sql
import hashlib as hl
import json
import os
from datetime import datetime

class Data_Manager():
    def connect_to_database():
        connection = sql.connect("Data/local_database.db")
        cur = connection.cursor()
        return(connection, cur)
    
    def create_database(connection, cur):
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
                    direction BOOL NOT NULL,
                    PRIMARY KEY (name, type, direction)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS exceptions (
                    targetcondition VARCHAR(255) NOT NULL,
                    targettype VARCHAR(16) NOT NULL,
                    allowcondition VARCHAR(255) NOT NULL,
                    allowtype VARCHAR(16) NOT NULL,
                    whitelisttype BOOL NOT NULL,
                    direction BOOL NOT NULL,
                    PRIMARY KEY(targetcondition, targettype, allowcondition, allowtype, direction)
        )
        """)
        connection.commit()

    def insert_user(connection, cur, username, password):
        encrypted_pass = Data_Manager.encryptPassword(password)
        try:
            cur.execute("""
            INSERT INTO userdata (username, password) VALUES (?,?)           
            """, (username, encrypted_pass))
            connection.commit()
        except Exception as e:
            sql.IntegrityError()
            return("Unique Username is Required", e)
        
    def encrypt_password(password):
        return hl.sha256(password.encode()).hexdigest()
    
    def remove_user(connection, cur):
        cur.execute("""
            DELETE FROM userdata          
            """)
        connection.commit()

    def find_password(connection, cur, username):
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

    def remove_whitelist(type, target, iswhitelisted, direction, cur, connection):
        print("Removing Whitelist" + type + " " + target + " " + iswhitelisted + " " + direction)
        cur.execute("""
            DELETE FROM whitelists WHERE name=? AND type=? AND whitelisttype=?  AND direction=?          
            """, (target, type, iswhitelisted, direction))
        connection.commit()
        print("Whitelist removed")
        

    def add_whitelist(type, target, iswhitelisted, direction, cur, connection):
        print("Adding Whitelist" + type + " " + target + " " + iswhitelisted + " " + direction)
        try:
            cur.execute("""
                INSERT INTO whitelists (name, type, whitelisttype, direction) VALUES (?, ?, ?, ?)           
                """, (target, type, iswhitelisted, direction))
            connection.commit()
            print("Whitelist Added")
            return("Added")
        except sql.IntegrityError() as Exception:
            return("Unique Whitelist is Required", Exception)
        
    def fetch_whitelists(cur, type):
        cur.execute("SELECT * FROM whitelists WHERE type IS ?", (type,))
        return cur.fetchall()
    
    def remove_exception(whitelist_type, direction, target_type, target_condition, allow_type, allow_condition, cur, connection):
        print("Removing Exception")
        cur.execute("""
            DELETE FROM exceptions WHERE targetcondition=? AND targettype=? AND allowcondition=? AND allowtype=? AND direction=? AND whitelisttype=?
            """, (target_condition, target_type, allow_condition, allow_type, direction, whitelist_type))
        connection.commit()
        print("Exception removed")
    
    def add_exception(whitelist_type, direction, target_type, target_condition, allow_type, allow_condition, cur, connection):
        print("Adding Exception")
        try:
            cur.execute("""
                INSERT INTO exceptions(targetcondition, targettype, allowcondition, allowtype, whitelisttype, direction) VALUES (?, ?, ?, ?, ?, ?)
                        """, (target_condition, target_type, allow_condition, allow_type, whitelist_type, direction))
            connection.commit()
            print("Excpetion Added")
            return("Added")
        except sql.IntegrityError() as Exception:
            return("Unique Exception is Required", Exception)
        
    def fetch_exceptions(cur):
        cur.execute("SELECT * FROM exceptions")
        return cur.fetchall()
    
    def append_to_or_create_log(rule_string):
        log_path = datetime.today().strftime("%Y-%m-%d")
        with open(log_path, "a+") as log_file:
            log_file.write(datetime.today().strftime("%H:%M:%S") + rule_string)

    def remove_log(log_name):
        filepath = "Data/Logs/"+os.fsdecode(log_name)
        os.remove(filepath)
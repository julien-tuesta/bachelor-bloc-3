import sqlite3
from pathlib import Path

# Define the paths
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
database_path = current_dir / "goldenline.db"

# hash des mots de passe
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# connection à la database
conn = sqlite3.connect(database_path, check_same_thread=False)

#gestion de la base de données utilisateurs
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def login_admin(username,password):
	c.execute('SELECT * FROM admintable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

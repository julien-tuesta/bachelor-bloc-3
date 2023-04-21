import sqlite3
from pathlib import Path
import hashlib
import query
import users
import pytest


# Define the paths
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
database_path = current_dir / "goldenline.db"

# connection à la database
conn = sqlite3.connect(database_path, check_same_thread=False)

def test_make_hashes():
    assert users.make_hashes("password") == hashlib.sha256(str.encode("password")).hexdigest()

def test_check_hashes():
    hashed_text = hashlib.sha256(str.encode("password")).hexdigest()
    assert users.check_hashes("password", hashed_text) == hashed_text
    assert not users.check_hashes("wrong_password", hashed_text)

def test_create_usertable():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    users.create_usertable()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='userstable';")
    assert c.fetchone()[0] == 'userstable'

def test_add_userdata():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    users.create_usertable()
    users.add_userdata('testuser', users.make_hashes('testpassword'))
    c.execute("SELECT * FROM userstable WHERE username = 'testuser';")
    user = c.fetchall()
    assert user[-1][1] == users.make_hashes('testpassword')

def test_login_user():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    users.create_usertable()
    users.add_userdata('testuser1', 'testpassword1')
    assert users.login_user('testuser1', 'testpassword1') != []
    assert users.login_user('testuser1', 'wrong_password1') == []

def test_view_all_users():
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    assert users.view_all_users()




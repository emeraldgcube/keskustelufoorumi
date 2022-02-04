from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,  password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
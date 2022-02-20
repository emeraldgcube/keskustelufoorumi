from db import db
from flask import session, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex
def login(username, password):
    sql = "SELECT id, password, rights FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["rights"] = user.rights
            session["csrf_token"] = token_hex(16)
            return True
        else:
            return False

def logout():
    session.clear()

def hasRights(wantedrights):
    if session["rights"] == wantedrights:
        return True
    return False

def changeRights(username, newrights):
    sql = "UPDATE users SET rights = :rights WHERE username = :username"
    db.session.execute(sql, {"rights":newrights, "username":username})
    db.session.commit()

def recordBan(username, message):
    user_id = findUserId(username)
    sql = "INSERT INTO bans (user_id, given_at, reason) VALUES (:user_id, NOW(), :message)"
    db.session.execute(sql, {"user_id":user_id, "message":message})
    db.session.commit()

def findUserId(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    userid = result.fetchone()
    return userid

def register(username, password):
    hash_value = generate_password_hash(password)
    if len(username) > 20 or len(username) == 0 or len(password) > 20 or len(password) < 5:
        return False
    try:
        sql = "INSERT INTO users (username, password, rights) VALUES (:username,:password, 'user')"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)
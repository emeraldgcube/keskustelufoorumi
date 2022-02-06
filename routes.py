from app import app
from db import db
from flask import render_template, request, redirect
import users

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/subforum")
def forum():
    sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql)
    messages = result.fetchall()

    return render_template("forum.html", messages=messages)
              
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/") 


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password'] 
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/subforum/send", methods=["GET", "POST"])
def send():
    if request.method == "GET":
        return render_template("send.html")
    if request.method == "POST":
        content = request.form["content"]
        user_id = users.user_id()
        if user_id == 0:
            return render_template("error.html", message="Et ole kirjautunut")
        sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
        db.session.execute(sql, {"content":content, "user_id":user_id})
        db.session.commit()
        return redirect("/subforum")


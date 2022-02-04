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
    result = db.session.execute("SELECT content FROM messages")
    messages = result.fetchall()
    return render_template("index.html", messages=messages) 


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/subforum/send", methods=["GET", "POST"])
def send():
    if request.method == "GET":
        return render_template("write.html")
    if request.method == "POST":
        content = request.form["content"]
        sql = "INSERT INTO messages (content) VALUES (:content)"
        db.session.execute(sql, {"content":content})
        db.session.commit()
        return redirect("/subforum")


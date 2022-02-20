from re import T
from app import app
from db import db
from flask import render_template, request, redirect, session, abort
import users
import topics
import messages

@app.route("/")
@app.route("/index")
def index():
    sql = "SELECT id, name, description FROM forums"
    result = db.session.execute(sql)
    forums = result.fetchall()
    return render_template("index.html", forums=forums)

@app.route("/subforum")
def forum():
    sql = "SELECT M.content, U.username, M.sent_at as id FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
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
            return render_template("error.html", message="Rekisteröinti ei onnistunut. Onhan käyttäjänimesi ja salasanasi maksimissaan 20 merkkiä pitkä ja salasana yli 5 merkin pituinen?")

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

@app.route("/testisivu")
def testisivu():
    return render_template("test.html")
    

@app.route("/topics/<int:id>")
def topic(id):
    sql = "SELECT M.content, U.username, M.sent_at as id FROM messages M, users U WHERE M.user_id=U.id and M.topic_id=:topicid ORDER BY M.id"
    result = db.session.execute(sql, {"topicid":id})
    messages = result.fetchall()
    return render_template("topic.html", messages=messages)

@app.route("/<int:id>")
def subforum(id):
    sql = "SELECT T.title, M.content, U.username, T.id FROM topics T, messages M, users U, forums F WHERE F.id = :id AND F.id = T.forum_id AND T.id=M.topic_id AND M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql, {"id":id})
    topics = result.fetchall()
    return render_template("forum.html", topics=topics)

@app.route("/topics/<int:topic_id>/newmessage", methods=["GET", "POST"])
@app.route("/<int:forum_id>/newtopic")
def send(forum_id, topic_id=None):
    if request.method == "GET":
        return render_template("send.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        title = request.form["title"]
        content = request.form["content"]
        sent = messages.checkMessage() 
        if sent == True:
            messages.sendMessage()
            return redirect("/subforum")
        return render_template("error.html", error=sent)

@app.route("/controlusers", methods=["GET", "POST"])
def controlusers():
    if not users.hasRights("admin"):
        return render_template("error.html", error="Sinulla ei ole oikeuksia tälle sivulle")

    if request.method == "GET" and users.hasRights("admin"):
        return render_template("controlusers.html")

    if request.method == "POST" and users.hasRights("admin"):
        newrights = request.form["newrights"]
        username = request.form["username"]
        users.changeRights(username, newrights)

        if newrights == "banned":
            reason = request.form["message"]
            users.recordBan(username, reason)

        return redirect("/index")
    return render_template("error.html", error="Jokin epäonnistui")
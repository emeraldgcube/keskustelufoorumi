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

@app.route("/<int:forum_id>/<int:topic_id>")
def topic(forum_id, topic_id):
    sql = "SELECT M.content, U.username, M.sent_at as id FROM messages M, users U WHERE M.user_id=U.id and M.topic_id=:topicid ORDER BY M.id"
    result = db.session.execute(sql, {"topicid":topic_id})
    messages = result.fetchall()
    return render_template("topic.html", messages=messages, forum_id=forum_id, topic_id=topic_id)

@app.route("/<int:forum_id>")
def subforum(forum_id):
    sql = "select distinct on (m.topic_id) m.topic_id, t.title,  u.username, m.content, m.sent_at from messages m left join topics t on m.topic_id = t.id left join users u on u.id = m.user_id where t.forum_id = :forum_id"
    result = db.session.execute(sql, {"forum_id":forum_id})
    topics = result.fetchall()
    return render_template("forum.html", topics=topics, forum_id=forum_id)

@app.route("/<int:forum_id>/<int:topic_id>/newmessage", methods=["GET", "POST"])
@app.route("/<int:forum_id>/newtopic", methods=["GET", "POST"])
def send(forum_id, topic_id=None):
    if request.method == "GET":
        return render_template("send.html", forum_id=forum_id, topic_id=topic_id)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        title = None
        if not topic_id:
            title = request.form["title"]
        content = request.form["content"]
        user_id = users.user_id()
        sent = messages.checkMessage(content, title) 
        if sent == True:
            messages.sendMessage(content, user_id, forum_id, title, topic_id)
            return redirect("/" + str(forum_id))
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
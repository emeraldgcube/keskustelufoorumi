from re import T
from app import app
from db import db
import sys
from flask import render_template, request, redirect, session, abort
import users
from forums import getForums
from topics import getForumTopics
from messages import getTopicContent, checkMessage, sendMessage

@app.route("/")
@app.route("/index")
def index():
    forums = getForums()
    return render_template("index.html", forums = forums)
              
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
            return render_template("error.html", message = "Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message = "Rekisteröinti ei onnistunut. Onhan käyttäjänimesi ja salasanasi maksimissaan 20 merkkiä pitkä ja salasana yli 5 merkin pituinen?")

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
            return render_template("error.html", message = "Väärä tunnus tai salasana")

@app.route("/<int:forum_id>/<int:topic_id>")
def topic(forum_id, topic_id):
    messages, title = getTopicContent(topic_id)
    return render_template("topic.html", messages = messages, title = title, forum_id = forum_id, topic_id = topic_id)

@app.route("/<int:forum_id>")
def subforum(forum_id):
    topics = getForumTopics(forum_id)
    return render_template("forum.html", topics=topics, forum_id=forum_id)

# same route for creating new topic or message. template differs by having/not having title input. maybe a bit messy but atleast no copypasta lol
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
        sent = checkMessage(content, title) 
        if sent == True:
            sendMessage(content, user_id, forum_id, title, topic_id)
            return redirect("/" + str(forum_id))
        return render_template("error.html", message = sent)



@app.route("/controlusers", methods=["GET", "POST"])
def controlusers():
    rights = users.getRights()
    if rights not in ("admin", "moderator"):
        return render_template("error.html", message = "Sinulla ei ole oikeuksia tälle sivulle")

    if request.method == "GET":
        return render_template("controlusers.html")

    if request.method == "POST" and rights == "admin":
        newrights = request.form["newrights"]
        username = request.form["username"]
        if newrights == "admin":
            if rights != "admin":
                return render_template("error.html", message = "Sinulla ei ole oikeuksia antaa admin-oikeuksia")
        users.changeRights(username, newrights)

        if newrights == "banned":
            reason = request.form["banreason"]
            users.recordBan(username, reason)

        return redirect("/index")
    return render_template("error.html", message = "Jokin epäonnistui")
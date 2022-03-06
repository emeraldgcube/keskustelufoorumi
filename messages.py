from curses.ascii import NUL
from db import db
import users
import sys

def getTopicContent(topic_id):
    sql = "SELECT M.content, U.username, M.sent_at  FROM messages M, users U WHERE M.user_id=U.id and M.topic_id=:topic_id ORDER BY M.id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    messages = result.fetchall()
    sql = "SELECT title FROM topics WHERE id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    title = result.fetchone()
    return messages, title


def sendMessage(content, user_id, forum_id, title, topic_id):
    if title:
        sql = "INSERT INTO topics (title, forum_id) VALUES (:title, :forum_id, :user_id) RETURNING id"
        topic_id = db.session.execute(sql, {"title":title, "forum_id":forum_id, "user_id":user_id,}).fetchone()[0]
        db.session.commit()
    sql = "INSERT INTO messages (content, user_id, sent_at, topic_id) VALUES (:content, :user_id, NOW(), :topic_id)"
    db.session.execute(sql, {"content":content, "user_id":user_id, "topic_id":topic_id})
    db.session.commit()

### palauttaa True jos viesti on sopiva, virheilmoituksen jos viallinen
def checkMessage(content, title):
    user_id = users.user_id()
    rights = users.getRights()
    if user_id == 0:
        return "Et ole kirjautunut"
    if title:
        if len(title) > 100:
            return "Otsikko on liian pitkä"
    if len(content) > 5000:
        return "Viesti on liian pitkä"
    if title == "" or not content:
        return "Otsikko tai viesti puuttuu"
    if rights == "banned":
        reason = users.getBanReason()
        return f"Sinulla ei ole oikeutta postata, syy: {reason[0]} \n banni annettu: {reason[1]}"
    return True
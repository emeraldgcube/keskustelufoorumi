from db import db
import users
def sendMessage(content, user_id, forum):
    sql = "INSERT INTO messages (content, user_id, sent_at, forum_id) VALUES (:content, :user_id, NOW(), :forum_id)"
    db.session.execute(sql, {"content":content, "user_id":user_id, "forum_id":forum})
    db.session.commit()

def findMessageById(message_id):
    sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id = U.id and M.id = :message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    message = result.fetchone()
    return message

### palauttaa True jos viesti on sopiva, virheilmoituksen jos viallinen
def checkMessage(content, title):
    user_id = users.user_id()
    if user_id == 0:
        return "Et ole kirjautunut"
    if len(title) > 100:
        return "Otsikko on liian pitkä"
    if len(content) > 5000:
        return "Viesti on liian pitkä"
    if not title or not content:
        return "Otsikko tai viesti puuttuu"
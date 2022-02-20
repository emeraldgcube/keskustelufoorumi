from db import db
def getTopicMessages(topic):
    sql = "SELECT T.title, U.username, M.sent_at, U.user FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql, {"topic":topic})
    messages = result.fetchall()

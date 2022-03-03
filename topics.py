from db import db

def getForumTopics(forum_id):
    sql = "select distinct on (m.topic_id) m.topic_id, t.title,  u.username, m.content, m.sent_at from messages m left join topics t on m.topic_id = t.id left join users u on u.id = m.user_id where t.forum_id = :forum_id"
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchall()
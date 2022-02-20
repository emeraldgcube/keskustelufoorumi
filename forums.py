from db import db
def getForumTopics(forum):
    sql = "SELECT T.title, M.content, U.username FROM topics T, messages M, users U, forums F WHERE F.id = :id AND F.id = T.forum_id AND T.id=M.topic_id AND M.user_id=U.id ORDER BY M.id"
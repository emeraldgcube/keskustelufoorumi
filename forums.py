from db import db
def getForums():
    sql = "SELECT id, name, description FROM forums"
    result = db.session.execute(sql)
    return result.fetchall()
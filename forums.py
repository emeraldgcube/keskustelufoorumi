from db import db
def getForums():
    sql = "SELECT id, name, description, hidden FROM forums"
    result = db.session.execute(sql)
    return result.fetchall()
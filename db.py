from app import app
from flask_sqlalchemy import SQLAlchemy
import os
import re

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app.config["SQLALCHEMY_DATABASE_URI"] = uri
db = SQLAlchemy(app)

import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def init_database():
    mydb = mysql.connector.connect(
    host="db",
    user="root",
    port="3306",
    password="pass"
    )

    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS issue_twitter")


def init_db(app):
    init_database()
    # mysql
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:pass@db:3306/issue_twitter?charset=utf8"
    db.init_app(app)
    Migrate(app, db)

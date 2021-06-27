import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@db:3306/issue_twitter?charset=utf8'
    db = SQLAlchemy()
    db.init_app(app)
    return db

    #with app.app_context():
    #    db.create_all()
    #Migrate(app, db)
    #
    #class User(db.Model):
    #    id = db.Column(db.Integer, primary_key=True)
    #    name = db.Column(db.String(128))
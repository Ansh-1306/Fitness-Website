from flask import Flask, render_template
import mysql.connector
from models import Class


        
app = Flask(__name__)

connection = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="fitness"
)

cursor = connection.cursor()

def load_classes_from_db():    
    try:
        cursor.execute("select * from classes")
        list_classes=cursor.fetchall()
        connection.commit()
        
        classes=[]

        for c in list_classes:
            cl = Class(c[0],c[1],c[2],c[3],c[4],c[5],c[6])
            classes.append(cl)

        return classes        
    except mysql.connector.Error as e:
        print(e)
    

@app.route("/")
@app.route("/home")
def home_page():
    classes = load_classes_from_db()

    return render_template('home.html', classes = classes, login=False)


@app.route("/login")
def login_page():
    return render_template('login.html', login=True)

    

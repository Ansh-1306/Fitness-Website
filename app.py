from flask import Flask, render_template, request
import mysql.connector
from models import Class


        
app = Flask(__name__)

connection = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="fitness"
)


global isLoggedIn 
isLoggedIn = False

def load_classes_from_db():    
    try:
        cursor = connection.cursor()    
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
    finally:
        cursor.close()


@app.route("/")
@app.route("/home")
def home_page():
    classes = load_classes_from_db()
    global isLoggedIn
    isLoggedIn = False
    return render_template('home.html', classes = classes, login=False, isLoggedIn = isLoggedIn)


@app.route("/login")
def login_page():
    global isLoggedIn
    isLoggedIn = False
    return render_template('login.html', login=True, isLoggedIn = False)

@app.route("/sign_up", methods=['POST','GET'])
def sign_up():
    try:
        global isLoggedIn
        cursor = connection.cursor()   
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        cpassword = request.form['cpassword']
        age = request.form['age']
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        cursor.execute('select * from users')
        list_users = cursor.fetchall()
        for user in list_users:
            if user[2] == phone:
                msg =  "User already exists!"
                isLoggedIn = False
                return render_template('login.html', isLoggedIn = isLoggedIn, msg=msg )
        if cpassword == password:
            insert_query = "INSERT INTO users(name, phone, age, height, weight, gender, password) VALUES ('"+name+"','"+phone+"',"+age+","+height+","+weight+",'"+gender+"','"+password+"')"
            cursor.execute(insert_query)
            connection.commit()
            if(cursor.rowcount>0):
                msg = "Account Created Successfully" 
                isLoggedIn = True
                classes = load_classes_from_db()
                return render_template('home.html', classes = classes, isLoggedIn = isLoggedIn)
            else:
                msg = "There was an error during sign up. Please Try Again!"
        else:
            msg = "Password does not match"
            isLoggedIn = False
        return render_template('login.html', isLoggedIn = isLoggedIn, msg = msg)
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
    


@app.route("/sign-in", methods=['POST','GET'])
def login():
    try:
        global isLoggedIn
        cursor = connection.cursor()   
        phone = request.form['phone']
        password = request.form['password']
    
        cursor.execute('select * from users')
        list_users = cursor.fetchall()
        for user in list_users:
            if user[2] == phone:
                if user[7] == password:
                    msg = "Account Created Successfully"
                    isLoggedIn = True
                    classes = load_classes_from_db()
                    return render_template('home.html', classes = classes, login=False, isLoggedIn = isLoggedIn)
                else:
                    msg = "Incorrect Password"
            else:
                msg = "User does not exist. Please Sign Up first "

        connection.commit()
        isLoggedIn = False
        return render_template('login.html', login=True, isLoggedIn = isLoggedIn, msg = msg)
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()


    

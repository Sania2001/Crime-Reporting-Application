import flask
import sqlite3

from flask import Flask, render_template,request,session,redirect
from flask_session import Session


conn = sqlite3.connect("crimeManagement.db", check_same_thread=False)
cursor = conn.cursor()

listOfTables = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name= 'crime' ").fetchall()

if listOfTables!=[]:
    print("Table Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE crime(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT, 
                            date int,  
                            description TEXT, 
                            remarks TEXT); ''')
print("Table has created")



listOfTables = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='user' ").fetchall()

if listOfTables!=[]:
    print("User table already exists !")

else:
    conn.execute(''' CREATE TABLE user(
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                mname TEXT, 
                                address TEXT, 
                                emailid TEXT, 
                                phone INTEGER,
                                mpassword TEXT); ''')
    print("User table has created !")



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        getUsername = request.form["username"]
        getppass = request.form["password"]

        if getUsername == "admin":
            if getppass == "12345":
                return redirect("/admin")
    return render_template("login.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin.html")


@app.route("/view")
def view():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crime")
    res = cursor.fetchall()
    return render_template("viewall.html", crime=res)


@app.route("/viewdate", methods=["GET", "POST"])
def viewdate():
    if request.method == "POST":
        getdate = request.form["date"]
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM crime WHERE date = '"+getdate+"' ")
        result = cursor.fetchall()
        return render_template("viewBydate.html", crime=result)
    return render_template("viewdate.html")


@app.route("/user", methods = ["GET","POST"])
def registerUser():

    if request.method == "POST":
        getMName = request.form["mname"]
        getAddress = request.form["address"]
        getEmailid = request.form["emailid"]
        getPhone = request.form["phone"]
        getPassword = request.form["mpassword"]

        print(getMName)
        print(getAddress)
        print(getEmailid)
        print(getPhone)
        print(getPassword)

        try:
            conn.execute("INSERT INTO user( mname, address, emailid, phone, mpassword)VALUES('"+getMName+"','"+getAddress+"','"+getEmailid+"','"+getPhone+"','"+getPassword+"')")
            print("Successfully inserted")
            conn.commit()
            return redirect("/userpage")

        except Exception as e:
            print(e)
    return render_template("user_register.html")


@app.route("/", methods=['GET','POST'])
def userlogin():
    if request.method == "POST":
        getEmailid = request.form["emailid"]
        getPassword = request.form["mpassword"]
        print(getEmailid)
        print(getPassword)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE emailid = '" + getEmailid + "' AND mpassword = '" + getPassword + "'")
        res2 = cursor.fetchall()
        if len(res2) > 0:
            for i in res2:
                getName = i[1]
                getid = i[0]

            session["name"] = getName
            session["id"] = getid

            return redirect("/userpage")

    return render_template("userlogin.html")


@app.route("/crimeEntry", methods = ["GET","POST"])
def CrimeEntry():

    if request.method == "POST":
        getName = request.form["name"]
        getDate = request.form["date"]
        getDescription = request.form["description"]
        getRemarks = request.form["remarks"]

        print(getName)
        print(getDate)
        print(getDescription)
        print(getRemarks)
        try:
            conn.execute("INSERT INTO crime(name, date, description, remarks )VALUES('"+getName+"','"+getDate+"','"+getDescription+"','"+getRemarks+"')")
            print("Successfully inserted")
            conn.commit()

        except Exception as e:
            print(e)
    return render_template("crimeEntry.html")


@app.route("/edit", methods = ['GET','POST'])
def edit():
        if request.method == "POST":
            getPhone = request.form["phone"]

            getMName = request.form["mname"]
            getAddress = request.form["address"]
            getEmailid = request.form["emailid"]
            getPassword = request.form["mpassword"]

            conn.execute("UPDATE user SET mname = '" + getMName + "',address ='" + getAddress + "',emailid = '" + getEmailid + "', mpassword = '"+getPassword+"' WHERE phone = '" + getPhone + "' ")
            print("successfully Updated !")
            conn.commit()

        return render_template("edit.html")


@app.route("/userpage", methods = ['GET','POST'])
def UserPage():
    return render_template("userpage.html")


@app.route("/guestuser", methods = ["GET","POST"])
def GuestCrimeEntry():

    if request.method == "POST":

        getDate = request.form["date"]
        getDescription = request.form["description"]
        getRemarks = request.form["remarks"]

        print(getDate)
        print(getDescription)
        print(getRemarks)
        try:
            conn.execute("INSERT INTO crime(date, description, remarks )VALUES('"+getDate+"','"+getDescription+"','"+getRemarks+"')")
            print("Successfully inserted")
            conn.commit()

        except Exception as e:
            print(e)
    return render_template("guest.html")


if(__name__) == "__main__":
    app.run(debug=True)

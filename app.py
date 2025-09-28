import sqlite3
from flask import Flask 
from flask import redirect, render_template, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

#front pg
@app.route("/")
def index():
    return render_template("index.html")

#New report
@app.route("/new_report")
def new_report():
    return render_template("new_report.html")

#@app.route("/create_item", methods=["POST"])
#def create_item():
#    title = request.form["title"]
#    description = request.form["description"]

#registration pg
@app.route("/register")
def register():
    return render_template("register.html")

#create password/register
@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not username or not password1 or not password2:
        return render_template("register.html", error="Fill in all fields please.")
    if password1 != password2:
        return render_template("register.html", error="Passwords do not match, try again.")
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        password_hash = generate_password_hash(password1)
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("register.html", error="The username is already taken, try another.")

    return render_template("success.html")

#login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
 #   if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
        
    if not username or not password:
        return render_template("login.html", error="Fill in all fields please")

    if not username or not password:
        return render_template("login.html", error="Fill in all fields please")

    result = db.query("SELECT password_hash FROM users WHERE username = ?", [username])
    if not result:
        return render_template("login.html", error="Username cannot be found")

    password_hash = result[0]["password_hash"]
        
    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return render_template("login.html", error="Wrong username or password.")

#logout
@app.route("/logout")
def logout():
    del session["username"]
    flash("You have successfully signed out of")
    return redirect("/")

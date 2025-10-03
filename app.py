import sqlite3
from flask import Flask 
from flask import redirect, render_template, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import items

app = Flask(__name__)
app.secret_key = config.secret_key

#front pg
@app.route("/")
def index():
    reports = items.get_items()  # fetch reports from database items-table
    return render_template("index.html", reports=reports)

@app.route("/report/<int:report_id>")
def show_report(report_id):
    report = items.get_report(report_id)
    if not report:
        return "Report not found", 404
    return render_template("show_report.html", report=report)

#New report
@app.route("/new_report")
def new_report():

    return render_template("new_report.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    title = request.form["title"]
    description = request.form["description"]
    travel_date = request.form["travel_date"]
    username = session["username"]
    # Make sure fields ar enot empty
    if not title or not description or not travel_date:
        return render_template("new_report.html", error="Please fill in all fields.")
    # add travel report to database
    items.add_item(username, title, description, travel_date)

    return redirect("/")  # directs user to front pg


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
    #basic check
    if not username or not password1 or not password2:
        return render_template("register.html", error="Fill in all fields please.")
    #min length check
    if len(username) < 3:
        return render_template("register.html", error="Username must be at least 3 characters.")
    if len(password1) < 4:
        return render_template("register.html", error="Password must be at least 4 characters.")    
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

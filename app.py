import sqlite3
from flask import Flask 
from flask import redirect, render_template, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import reports
import re

app = Flask(__name__)
app.secret_key = config.secret_key

#front pg
@app.route("/")
def index():
    query = request.args.get("q", "").strip()  # search by searchword if given
    all_reports = reports.get_reports()
    # filter if searchword given
    if query:
        all_reports = [r for r in all_reports if query.lower() in r["title"].lower()]

    grouped = {}
    for r in all_reports:
        country = r["country"] or "Unknown"
        if country not in grouped:
            grouped[country] = []
        grouped[country].append(r)

    # countries in alphabetical order
    sorted_grouped = dict(sorted(grouped.items()))
    return render_template("index.html", grouped=sorted_grouped)

#New report
@app.route("/new_report")
def new_report():

    return render_template("new_report.html")

@app.route("/create_report", methods=["POST"])
def create_report():
    title = request.form["title"]
    description = request.form["description"]
    travel_date = request.form["travel_date"]
    username = session["username"]
    country = request.form["country"]

    # Make sure fields are not empty
    if not title or not description or not travel_date:
        return render_template(
            "new_report.html",
            error="Please fill in all fields.",
            title=title,
            description=description,
            country=country,
            travel_date=travel_date
        )

    # Date form check (MM/YYYY)
    if not re.match(r"^\d{2}/\d{4}$", travel_date):
        return render_template(
            "new_report.html",
            error="Please use format MM/YYYY.",
            title=title,
            description=description,
            country=country,
            travel_date=travel_date
        )

    # Check sensible month
    month, year = travel_date.split("/")
    if not (1 <= int(month) <= 12):
        return render_template(
            "new_report.html",
            error="Month must be between 01 and 12.",
            title=title,
            description=description,
            country=country,
            travel_date=travel_date
        )

    # Save report
    reports.add_report(username, title, description, travel_date, country)
    return redirect("/")

@app.route("/report/<int:report_id>")
def show_report(report_id):
    report = reports.get_report(report_id)
    if not report:
        return "Report not found", 404
    return render_template("show_report.html", report=report)

#shows edit report sheet
@app.route("/report/<int:report_id>/edit")
def edit_report(report_id):
    report = reports.get_report(report_id)
    if not report:
        return "Report not found", 404
    if report["username"] != session.get("username"):
        return "Unauthorized", 403

    return render_template("edit_report.html", report=report)

#updates edited report
@app.route("/report/<int:report_id>/update", methods=["POST"])
def update_report(report_id):
    report = reports.get_report(report_id)
    if not report:
        return "Report not found", 404
    if report["username"] != session.get("username"):
        return "Unauthorized", 403

    title = request.form["title"]
    description = request.form["description"]
    travel_date = request.form["travel_date"]
    country = request.form["country"]

    reports.update_report(report_id, title, description, travel_date, country)
    return redirect(f"/report/{report_id}")

#delete report
@app.route("/report/<int:report_id>/delete")
def delete_report(report_id):
    report = reports.get_report(report_id)
    if not report:
        return "Report not found", 404
    if report["username"] != session.get("username"):
        return "Unauthorized", 403

    reports.delete_report(report_id)
    return redirect("/")

@app.route("/user/<username>")
def user_page(username):
    all_reports = reports.get_reports()
    user_reports = [r for r in all_reports if r["username"] == username]

    total_reports = len(user_reports)
    countries = sorted(set(r["country"] or "Unknown" for r in user_reports))

    return render_template(
        "user_page.html",
        username=username,
        reports=user_reports,
        total_reports=total_reports,
        countries=countries
    )

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

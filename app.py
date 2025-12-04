import os
import sqlite3
from flask import Flask, redirect, render_template, request, session, flash, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import config
import db
import reports
import re
import classes
import users
import comments
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "username" not in session:
        flash("Please log in to continue.")
        return redirect("/login")

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

# Pic settings
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# check function for uploaded files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# front page
@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    all_reports = reports.get_reports()

    if query:
        all_reports = [
            r for r in all_reports
            if query.lower() in r["title"].lower()
            or query.lower() in (r["country"] or "").lower()
        ]

    grouped = {}
    for r in all_reports:
        country = r["country"] or "Unknown country"
        grouped.setdefault(country, []).append(r)

    sorted_grouped = dict(
        sorted(grouped.items(), key=lambda item: (item[0] == "Unknown country", item[0]))
    )

    if query and not all_reports:
        flash("No results found for your search.")

    return render_template("index.html", grouped=sorted_grouped)

# new report
@app.route("/new_report", methods=["GET"])
def new_report():
    if "username" not in session:
        flash("Please log in to continue.")
        return redirect("/login")

    holiday_types = classes.get_holiday_types()
    themes = classes.get_themes()

    return render_template("new_report.html", holiday_types=holiday_types, themes=themes)

@app.route("/create_report", methods=["POST"])
def create_report():
    require_login()
    check_csrf()

    title = request.form.get("title", "").strip()
    if title:
        title = title[0].upper() + title[1:]
    description = request.form.get("description", "").strip()
    travel_date = request.form.get("travel_date", "").strip()
    username = session["username"]
    country = request.form.get("country", "").strip().title()
    section = request.form.get("section", "").strip()
    theme = request.form.get("theme", "").strip()

    if not title or not description or not travel_date or not section or not theme:
        holiday_types = classes.get_holiday_types()
        themes = classes.get_themes()
        return render_template("new_report.html",
            error="Please fill in all fields.",
            title=title, description=description, country=country,
            travel_date=travel_date, holiday_types=holiday_types, themes=themes
        )

    # Date validation (MM/YYYY)
    if not re.match(r"^\d{2}/\d{4}$", travel_date):
        holiday_types = classes.get_holiday_types()
        themes = classes.get_themes()
        return render_template("new_report.html",
            date_error="Please use format MM/YYYY.",
            title=title, description=description, country=country,
            travel_date=travel_date, holiday_types=holiday_types, themes=themes
        )

    month, year = travel_date.split("/")
    if not (1 <= int(month) <= 12):
        holiday_types = classes.get_holiday_types()
        themes = classes.get_themes()
        return render_template("new_report.html",
            date_error="Month must be between 01 and 12.",
            title=title, description=description, country=country,
            travel_date=travel_date, holiday_types=holiday_types, themes=themes
        )

    current_year = datetime.now().year
    year_int = int(year)
    if year_int < 1920 or year_int > current_year:
        holiday_types = classes.get_holiday_types()
        themes = classes.get_themes()
        return render_template("new_report.html",
            date_error=f"Year must be between 1920 and {current_year}.",
            title=title, description=description, country=country,
            travel_date=travel_date, holiday_types=holiday_types, themes=themes
        )

    report_id = reports.add_report(username, title, description, travel_date, country, section, theme)

    if "images" in request.files:
        files = request.files.getlist("images")
        for file in files[:5]:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return redirect(f"/report/{report_id}")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/report/<int:id>", methods=["GET", "POST"])
def report_page(id):
    if request.method == "POST":
        require_login()
        check_csrf()
        if "username" not in session:
            return redirect("/login")
        content = request.form["content"].strip()
        if content:
            db.add_comment(id, session["username"], content)
        return redirect(f"/report/{id}")

    report = reports.get_report(id)
    if not report:
        return "Report not found", 404

    all_comments = comments.get_comments(id)
    images = reports.get_images(id)
    return render_template("show_report.html", report=report, comments=all_comments, images=images)

# edit report
@app.route("/report/<int:report_id>/edit")
def edit_report(report_id):
    report = reports.get_report(report_id)
    if not report:
        return "Report not found", 404
    if report["username"] != session.get("username"):
        return "Unauthorized", 403

    holiday_types = classes.get_holiday_types()
    themes = classes.get_themes()
    images = reports.get_images(report_id)

    return render_template("edit_report.html", report=report,
        holiday_types=holiday_types, themes=themes, images=images)

@app.route("/image/<int:image_id>/delete")
def delete_image(image_id):
    if "username" not in session:
        return redirect("/login")
    reports.delete_image(image_id, session["username"])
    flash("Image deleted.")
    return redirect(request.referrer or "/")

# update report
@app.route("/report/<int:report_id>/update", methods=["POST"])
def update_report(report_id):
    require_login()
    check_csrf()

    report = reports.get_report(report_id)
    if not report:
        return "Report not found", 404
    if report["username"] != session.get("username"):
        return "Unauthorized", 403

    title = request.form.get("title", "").strip()
    if title:
        title = title[0].upper() + title[1:]
    description = request.form.get("description", "").strip()
    travel_date = request.form.get("travel_date", "").strip()
    country = request.form.get("country", "").strip().title()
    section = request.form.get("section", "").strip()
    theme = request.form.get("theme", "").strip()

    # Date validation with flash instead of red text
    if not re.match(r"^\d{2}/\d{4}$", travel_date):
        flash("Please use format MM/YYYY.")
        return redirect(request.referrer or f"/report/{report_id}/edit")

    month, year = travel_date.split("/")
    if not (1 <= int(month) <= 12):
        flash("Month must be between 01 and 12.")
        return redirect(request.referrer or f"/report/{report_id}/edit")

    current_year = datetime.now().year
    year_int = int(year)
    if year_int < 1920 or year_int > current_year:
        flash(f"Year must be between 1920 and {current_year}.")
        return redirect(request.referrer or f"/report/{report_id}/edit")

    # if everything is fine, update report normally
    reports.update_report(report_id, title, description, travel_date, country, section, theme)

    if "images" in request.files:
        files = request.files.getlist("images")
        for file in files[:5]:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                db.execute(
                    "INSERT INTO report_images (report_id, filename) VALUES (?, ?)",
                    [report_id, filename]
                )

    flash("Report updated successfully.")
    return redirect(f"/report/{report_id}")

# delete report
@app.route("/report/<int:report_id>/delete")
def delete_report(report_id):
    report = reports.get_report(report_id)
    if not report:
        return "Report not found", 404
    if report["username"] != session.get("username"):
        return "Unauthorized", 403
    reports.delete_report(report_id, session["username"])
    return redirect("/")

@app.route("/user/<username>")
def user_page(username):
    all_reports = reports.get_reports()
    user_reports = [r for r in all_reports if r["username"] == username]
    total_reports = len(user_reports)
    countries = sorted(set(r["country"] or "Unknown" for r in user_reports))
    return render_template("user_page.html", username=username,
        reports=user_reports, total_reports=total_reports, countries=countries)

# registration and login
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    check_csrf()
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username or not password1 or not password2:
        return render_template("register.html", error="Fill in all fields please.")
    if len(username) < 3:
        return render_template("register.html", error="Username must be at least 3 characters.")
    if len(password1) < 4:
        return render_template("register.html", error="Password must be at least 4 characters.")
    if password1 != password2:
        return render_template("register.html", error="Passwords do not match, try again.")

    success = users.add_user(username, password1)
    if not success:
        return render_template("register.html", error="The username is already taken, try another.")

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        return render_template("login.html", error="Fill in all fields please")
    if not users.verify_login(username, password):
        return render_template("login.html", error="Invalid username or password")

    session["username"] = username
    session["csrf_token"] = secrets.token_hex(16)
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    flash("You have successfully signed out.")
    return redirect("/")

@app.route("/comment/<int:comment_id>/delete", methods=["POST"])
def delete_comment(comment_id):
    require_login()
    check_csrf()
    comments.delete_comment(comment_id, session["username"])
    flash("Comment deleted.")
    return redirect(request.referrer or "/")

@app.route("/my_comments")
def my_comments():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    user_comments = comments.get_comments_by_user(username)
    return render_template("my_comments.html", comments=user_comments)

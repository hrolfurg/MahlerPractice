import csv
import json
import os
from functools import wraps
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, send_from_directory, flash
)

app = Flask(__name__)
app.secret_key = "mh8-practice-secret-2024-xQ7pL"

USERNAME = "mahler"
PASSWORD = "mahler"

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "voices.csv")
MP3_DIR = os.path.join(os.path.dirname(__file__), "mp3")


def load_data():
    rows = []
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "voice": row["Voice"].strip(),
                "choir": row["Choir"].strip(),
                "voice_type": row["Voice type"].strip(),
                "part": row["Part"].strip(),
                "section": row["Section"].strip(),
                "filename": row["MP3 filename"].strip(),
            })
    return rows


TRACK_DATA = load_data()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("index"))
    error = None
    if request.method == "POST":
        if (request.form.get("username") == USERNAME and
                request.form.get("password") == PASSWORD):
            session["logged_in"] = True
            return redirect(url_for("index"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template("index.html", track_data=json.dumps(TRACK_DATA))


@app.route("/mp3/<path:filename>")
@login_required
def serve_mp3(filename):
    return send_from_directory(MP3_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

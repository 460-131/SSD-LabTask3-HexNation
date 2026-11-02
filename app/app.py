import os, sqlite3, subprocess, json
import requests
from flask import Flask, request, session, send_from_directory, render_template_string

app = Flask(__name__)
app.secret_key = os.environ.get("SMARTCAMPUS_SECRET_KEY", "fallback-dev-key")
DB = "smartcampus.db"
GATEWAY_TOKEN = os.environ.get("GATEWAY_TOKEN", "fallback-token")

def db():
    return sqlite3.connect(DB)

def require_role(*roles):
    def deco(fn):
        def wrapper(*a, **k):
            if session.get("role") not in roles:
                return "Forbidden", 403
            return fn(*a, **k)
        wrapper.__name__ = fn.__name__
        return wrapper
    return deco

@app.route("/login", methods=["POST"])
def login():
    user = request.form["username"]
    pwd = request.form["password"]
    row = db().execute("SELECT id FROM users WHERE name=? AND pw=?", (user, pwd)).fetchone()
    if row:
        session["uid"] = row[0]
        session["role"] = "student"
        return "OK"
    return "Invalid"

@app.route("/grades")
def grades():
    sid = request.args.get("student_id")
    if str(session.get("uid")) != sid:
        return "Forbidden", 403
    rows = db().execute("SELECT course, marks FROM grades WHERE student_id=?", (sid,)).fetchall()
    return str(rows)

@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return render_template_string("<h1>Welcome {{ name }}</h1>", name=name)

@app.route("/download")
def download():
    return send_from_directory("uploads", request.args.get("file", ""))

@app.route("/report")
def report():
    dept = request.args.get("dept")
    ALLOWED = {"cs", "ee", "math"}
    if dept not in ALLOWED:
        return "Bad department", 400
    return subprocess.check_output(["python", "make_report.py", dept])

@app.route("/calc")
def calc():
    return "Math is disabled for security", 400

@app.route("/restore", methods=["POST"])
def restore():
    try:
        return str(json.loads(request.data))
    except:
        return "Invalid JSON", 400

@app.route("/fees")
def fees():
    r = requests.get("https://gateway.example.com/status", verify=True, timeout=10)
    return r.text

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False)

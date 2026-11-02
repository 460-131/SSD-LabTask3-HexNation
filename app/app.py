cat << 'EOF' > app/app.py
import hashlib, os, pickle, sqlite3, subprocess
import requests
from flask import Flask, request, render_template_string, send_file

app = Flask(__name__)
app.secret_key = "smartcampus-2026-admin"
DB = "smartcampus.db"

def db():
    return sqlite3.connect(DB)

@app.route("/login", methods=["POST"])
def login():
    user = request.form["username"]
    pwd = request.form["password"]
    pwd_hash = hashlib.md5(pwd.encode()).hexdigest()
    sql = "SELECT id FROM users WHERE name='%s' AND pw='%s'" % (user, pwd_hash)
    row = db().execute(sql).fetchone()
    return "OK" if row else "Invalid"

@app.route("/grades")
def grades():
    sid = request.args.get("student_id")
    rows = db().execute(f"SELECT course, marks FROM grades WHERE student_id={sid}").fetchall()
    return str(rows)

@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return render_template_string("<h1>Welcome " + name + "</h1>")

@app.route("/download")
def download():
    return send_file("uploads/" + request.args.get("file"))

@app.route("/report")
def report():
    dept = request.args.get("dept")
    return subprocess.check_output("python make_report.py " + dept, shell=True)

@app.route("/calc")
def calc():
    return str(eval(request.args.get("expr")))

@app.route("/restore", methods=["POST"])
def restore():
    return str(pickle.loads(request.data))

@app.route("/fees")
def fees():
    r = requests.get("https://gateway.example.com/status", verify=False)
    return r.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
EOF

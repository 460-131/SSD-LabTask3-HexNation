import hashlib, os, pickle, sqlite3, subprocess
import requests
from flask import Flask, request, render_template_string, send_file
app = Flask(__name__)
SECRET_KEY = &quot;smartcampus-2026-admin&quot;
DB = &quot;smartcampus.db&quot;
def db():
return sqlite3.connect(DB)
@app.route(&quot;/login&quot;, methods=[&quot;POST&quot;])
def login():
user = request.form[&quot;username&quot;]
pwd = request.form[&quot;password&quot;]
pwd_hash = hashlib.md5(pwd.encode()).hexdigest()
sql = &quot;SELECT id FROM users WHERE name=&#39;%s&#39; AND pw=&#39;%s&#39;&quot; % (user, pwd_hash)
row = db().execute(sql).fetchone()
return &quot;OK&quot; if row else &quot;Invalid&quot;
@app.route(&quot;/grades&quot;)
def grades():
sid = request.args.get(&quot;student_id&quot;)
rows = db().execute(f&quot;SELECT course, marks FROM grades WHERE student_id={sid}&quot;).fetchall()
return str(rows)
@app.route(&quot;/hello&quot;)
def hello():
name = request.args.get(&quot;name&quot;, &quot;&quot;)
return render_template_string(&quot;&lt;h1&gt;Welcome &quot; + name + &quot;&lt;/h1&gt;&quot;)
@app.route(&quot;/download&quot;)
def download():
return send_file(&quot;uploads/&quot; + request.args.get(&quot;file&quot;))
@app.route(&quot;/report&quot;)
def report():
dept = request.args.get(&quot;dept&quot;)
return subprocess.check_output(&quot;python make_report.py &quot; + dept, shell=True)
@app.route(&quot;/calc&quot;)
def calc():
return str(eval(request.args.get(&quot;expr&quot;)))
@app.route(&quot;/restore&quot;, methods=[&quot;POST&quot;])
def restore():
return str(pickle.loads(request.data))
@app.route(&quot;/fees&quot;)
def fees():
r = requests.get(&quot;https://gateway.example.com/status&quot;, verify=False)
return r.text
if __name__ == &quot;__main__&quot;:
app.run(host=&quot;0.0.0.0&quot;, debug=True)
# app/make_db.py : builds smartcampus.db for testing the fixes
import sqlite3
from werkzeug.security import generate_password_hash as g
c = sqlite3.connect(&#39;smartcampus.db&#39;)
c.execute(&#39;create table users(id integer primary key, name text, pw text)&#39;)
c.execute(&#39;create table grades(student_id integer, course text, marks int)&#39;)
c.execute(&#39;insert into users values(1, ?, ?)&#39;, (&#39;ali&#39;, g(&#39;pass123&#39;)))
c.executemany(&#39;insert into grades values(?,?,?)&#39;, [(1,&#39;SSDD&#39;,88),(2,&#39;DB&#39;,71)])
c.commit()
git add app/ &amp;&amp; git commit -m &quot;Add vulnerable practice code&quot; &amp;&amp; git push

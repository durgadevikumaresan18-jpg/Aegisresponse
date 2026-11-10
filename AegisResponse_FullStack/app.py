import os, sqlite3, math, json, uuid, base64, mimetypes, re
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

ROOT=os.path.dirname(os.path.abspath(__file__))
DB=os.path.join(ROOT,"aegisresponse.db")
app=Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key=os.getenv("FLASK_SECRET_KEY","change-this-development-secret")
app.config["MAX_CONTENT_LENGTH"]=8*1024*1024
CATEGORIES=["Fire Emergency","Road Accident","Medical Emergency","Flood","Building Collapse","Other Emergencies"]
SEVERITIES={"Low":15,"Medium":35,"High":65,"Critical":85}
TEAM_CATEGORIES={
 "Fire":["Fire Emergency","Building Collapse"],
 "Medical":["Medical Emergency","Road Accident"],
 "Rescue":["Flood","Building Collapse","Other Emergencies","Road Accident"],
 "Multi-purpose":CATEGORIES
}
def now(): return datetime.now(timezone.utc).isoformat()
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; c.execute("PRAGMA foreign_keys=ON"); return c
def init_db():
 with db() as c:
  c.executescript("""
  CREATE TABLE IF NOT EXISTS incidents(
   id TEXT PRIMARY KEY,title TEXT NOT NULL,description TEXT NOT NULL,category TEXT NOT NULL,
   severity TEXT NOT NULL,people INTEGER NOT NULL DEFAULT 0,location TEXT NOT NULL,
   latitude REAL,longitude REAL,contact TEXT,status TEXT NOT NULL DEFAULT 'Reported',
   priority_score INTEGER NOT NULL DEFAULT 0,assigned_team_id TEXT,photo_filename TEXT,
   created_at TEXT NOT NULL,updated_at TEXT NOT NULL,resolved_at TEXT,
   FOREIGN KEY(assigned_team_id) REFERENCES teams(id));
  CREATE TABLE IF NOT EXISTS teams(
   id TEXT PRIMARY KEY,name TEXT NOT NULL,response_category TEXT NOT NULL,
   supported_categories TEXT NOT NULL,latitude REAL NOT NULL,longitude REAL NOT NULL,
   availability TEXT NOT NULL DEFAULT 'Available',assigned_incident_id TEXT,
   created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS assignment_history(
   id INTEGER PRIMARY KEY AUTOINCREMENT,incident_id TEXT NOT NULL,team_id TEXT NOT NULL,
   action TEXT NOT NULL,distance_km REAL,created_at TEXT NOT NULL,
   FOREIGN KEY(incident_id) REFERENCES incidents(id),FOREIGN KEY(team_id) REFERENCES teams(id));
  CREATE TABLE IF NOT EXISTS admins(username TEXT PRIMARY KEY,password_hash TEXT NOT NULL);
  CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);
  CREATE INDEX IF NOT EXISTS idx_incidents_priority ON incidents(priority_score DESC);
  CREATE INDEX IF NOT EXISTS idx_teams_availability ON teams(availability);
  """)
  if not c.execute("SELECT 1 FROM admins WHERE username='admin'").fetchone():
   c.execute("INSERT INTO admins VALUES(?,?)",("admin",generate_password_hash(os.getenv("ADMIN_PASSWORD","admin123"))))
  if c.execute("SELECT COUNT(*) FROM teams").fetchone()[0]==0:
   seeds=[
    ("AMB-01","Ambulance Unit 01","Medical",["Medical Emergency","Road Accident"],13.0827,80.2707),
    ("FIR-01","Fire Response 01","Fire",["Fire Emergency","Building Collapse"],13.0569,80.2425),
    ("RES-01","Rescue Team 01","Rescue",["Flood","Building Collapse","Other Emergencies","Road Accident"],13.0400,80.2500),
    ("AMB-02","Ambulance Unit 02","Medical",["Medical Emergency","Road Accident"],13.0674,80.2376)]
   for x in seeds:c.execute("INSERT INTO teams(id,name,response_category,supported_categories,latitude,longitude,availability,created_at,updated_at) VALUES(?,?,?,?,?,?, 'Available',?,?)",(x[0],x[1],x[2],json.dumps(x[3]),x[4],x[5],now(),now()))
def rowdict(r):
 if not r:return None
 d=dict(r)
 for k in ("supported_categories",):
  if k in d:
   try:d[k]=json.loads(d[k])
   except:d[k]=[]
 return d
def allrows(sql,args=()):
 with db() as c:return [rowdict(x) for x in c.execute(sql,args).fetchall()]
def one(sql,args=()):
 with db() as c:return rowdict(c.execute(sql,args).fetchone())
def distance_km(lat1,lon1,lat2,lon2):
 r=6371.0088;p=math.pi/180
 a=math.sin((lat2-lat1)*p/2)**2+math.cos(lat1*p)*math.cos(lat2*p)*math.sin((lon2-lon1)*p/2)**2
 return 2*r*math.asin(math.sqrt(a))
def score(severity,people,category,created_at):
 age_hours=0
 try: age_hours=max(0,(datetime.now(timezone.utc)-datetime.fromisoformat(created_at.replace("Z","+00:00"))).total_seconds()/3600)
 except: pass
 cat_bonus=8 if category in ("Fire Emergency","Building Collapse") else 5 if category in ("Medical Emergency","Road Accident") else 0
 return min(99,round(SEVERITIES.get(severity,15)+min(max(0,int(people))*1.2,15)+cat_bonus+min(12,age_hours)))
def json_error(message,code=400):return jsonify(error=message),code
def admin_required(fn):
 @wraps(fn)
 def wrapped(*a,**kw):
  if not session.get("admin"):return json_error("Admin login required",401)
  return fn(*a,**kw)
 return wrapped
@app.get("/")
def user_page():return render_template("user.html")
@app.get("/admin")
def admin_page():return render_template("admin.html")
@app.get("/health")
def health():return jsonify(status="ok",service="AegisResponse")
@app.post("/api/admin/login")
def admin_login():
 d=request.get_json(silent=True) or {}
 a=one("SELECT * FROM admins WHERE username=?",(d.get("username",""),))
 if not a or not check_password_hash(a["password_hash"],d.get("password","")):return json_error("Invalid username or password",401)
 session["admin"]=a["username"];return jsonify(ok=True,username=a["username"])
@app.post("/api/admin/logout")
def admin_logout():session.clear();return jsonify(ok=True)
@app.get("/api/admin/session")
def admin_session():return jsonify(authenticated=bool(session.get("admin")),username=session.get("admin"))
@app.get("/api/incidents")
def list_incidents():
 refresh_priorities()
 status=request.args.get("status")
 sql="SELECT i.*,t.name AS assigned_team_name,t.response_category AS assigned_team_category FROM incidents i LEFT JOIN teams t ON t.id=i.assigned_team_id"
 args=()
 if status:sql+=" WHERE i.status=?";args=(status,)
 sql+=" ORDER BY i.priority_score DESC,i.created_at ASC"
 return jsonify(items=allrows(sql,args))
@app.post("/api/incidents")
def refresh_priorities():
 rows=allrows("SELECT id,severity,people,category,created_at FROM incidents")
 with db() as c:
  for x in rows:c.execute("UPDATE incidents SET priority_score=? WHERE id=?",(score(x["severity"],x["people"],x["category"],x["created_at"]),x["id"]))
def create_incident():
 d=request.get_json(silent=True) or {}
 required=["title","description","category","severity","location"]
 if any(not str(d.get(k,"")).strip() for k in required):return json_error("Title, description, category, severity and location are required.")
 if d["category"] not in CATEGORIES:return json_error("Invalid incident category.")
 if d["severity"] not in SEVERITIES:return json_error("Invalid severity.")
 try:people=max(0,min(100000,int(d.get("people",0))))
 except:return json_error("People affected must be a number.")
 try:lat=float(d["latitude"]) if d.get("latitude") not in (None,"") else None;lon=float(d["longitude"]) if d.get("longitude") not in (None,"") else None
 except:return json_error("Invalid coordinates.")
 if (lat is None)!=(lon is None):return json_error("Latitude and longitude must be supplied together.")
 if lat is not None and not(-90<=lat<=90 and -180<=lon<=180):return json_error("Coordinates are out of range.")
 created=now();iid="AEG-"+uuid.uuid4().hex[:8].upper();ps=score(d["severity"],people,d["category"],created)
 with db() as c:
  c.execute("""INSERT INTO incidents(id,title,description,category,severity,people,location,latitude,longitude,contact,status,priority_score,photo_filename,created_at,updated_at)
  VALUES(?,?,?,?,?,?,?,?,?,?, 'Reported',?,?,?,?)""",(iid,d["title"].strip(),d["description"].strip(),d["category"],d["severity"],people,d["location"].strip(),lat,lon,d.get("contact"),ps,d.get("photo_filename"),created,created))
 return jsonify(item=one("SELECT * FROM incidents WHERE id=?",(iid,))),201
@app.get("/api/incidents/<iid>")
def get_incident(iid):
 x=one("SELECT i.*,t.name AS assigned_team_name FROM incidents i LEFT JOIN teams t ON t.id=i.assigned_team_id WHERE i.id=?",(iid,))
 return (jsonify(item=x),200) if x else json_error("Incident not found",404)
@app.patch("/api/incidents/<iid>/status")
@admin_required
def update_incident_status(iid):
 d=request.get_json(silent=True) or {};status=d.get("status")
 if status not in ["Reported","Assigned","In Progress","Resolved"]:return json_error("Invalid incident status.")
 with db() as c:
  x=c.execute("SELECT * FROM incidents WHERE id=?",(iid,)).fetchone()
  if not x:return json_error("Incident not found",404)
  resolved=now() if status=="Resolved" else None
  c.execute("UPDATE incidents SET status=?,resolved_at=COALESCE(?,resolved_at),updated_at=? WHERE id=?",(status,resolved,now(),iid))
  if status=="Resolved" and x["assigned_team_id"]:
   c.execute("UPDATE teams SET availability='Available',assigned_incident_id=NULL,updated_at=? WHERE id=?",(now(),x["assigned_team_id"]))
 return jsonify(item=one("SELECT * FROM incidents WHERE id=?",(iid,)))
@app.delete("/api/incidents/<iid>")
@admin_required
def delete_incident(iid):
 with db() as c:
  x=c.execute("SELECT assigned_team_id FROM incidents WHERE id=?",(iid,)).fetchone()
  if not x:return json_error("Incident not found",404)
  if x["assigned_team_id"]:c.execute("UPDATE teams SET availability='Available',assigned_incident_id=NULL,updated_at=? WHERE id=?",(now(),x["assigned_team_id"]))
  c.execute("DELETE FROM assignment_history WHERE incident_id=?",(iid,));c.execute("DELETE FROM incidents WHERE id=?",(iid,))
 return jsonify(ok=True)
@app.get("/api/teams")
def list_teams():return jsonify(items=allrows("SELECT * FROM teams ORDER BY name"))
@app.post("/api/teams")
@admin_required
def create_team():
 d=request.get_json(silent=True) or {}
 try:lat=float(d["latitude"]);lon=float(d["longitude"])
 except:return json_error("Valid latitude and longitude are required.")
 if not(-90<=lat<=90 and -180<=lon<=180):return json_error("Coordinates out of range.")
 tid=str(d.get("id","")).strip();name=str(d.get("name","")).strip();cat=d.get("response_category")
 if not tid or not name or cat not in TEAM_CATEGORIES:return json_error("Team ID, name and valid response category are required.")
 cats=d.get("supported_categories") or TEAM_CATEGORIES[cat]
 if not isinstance(cats,list) or not cats or any(x not in CATEGORIES for x in cats):return json_error("Select valid supported incident categories.")
 try:
  with db() as c:c.execute("INSERT INTO teams VALUES(?,?,?,?,?,?, 'Available',NULL,?,?)",(tid,name,cat,json.dumps(cats),lat,lon,now(),now()))
 except sqlite3.IntegrityError:return json_error("Team ID already exists.")
 return jsonify(item=one("SELECT * FROM teams WHERE id=?",(tid,))),201
@app.patch("/api/teams/<tid>")
@admin_required
def update_team(tid):
 d=request.get_json(silent=True) or {};t=one("SELECT * FROM teams WHERE id=?",(tid,))
 if not t:return json_error("Team not found",404)
 if "availability" in d and d["availability"] not in ["Available","Busy","Offline"]:return json_error("Invalid availability.")
 if t["assigned_incident_id"] and d.get("availability")=="Available":return json_error("Resolve or unassign the incident before making this team available.")
 with db() as c:c.execute("UPDATE teams SET availability=?,updated_at=? WHERE id=?",(d.get("availability",t["availability"]),now(),tid))
 return jsonify(item=one("SELECT * FROM teams WHERE id=?",(tid,)))
@app.post("/api/incidents/<iid>/assign")
@admin_required
def assign_team(iid):
 d=request.get_json(silent=True) or {}
 with db() as c:
  inc=c.execute("SELECT * FROM incidents WHERE id=?",(iid,)).fetchone()
  if not inc:return json_error("Incident not found",404)
  if inc["status"]=="Resolved":return json_error("Resolved incidents cannot be assigned.")
  teams=c.execute("SELECT * FROM teams WHERE availability='Available'").fetchall()
  suitable=[]
  for t in teams:
   cats=json.loads(t["supported_categories"])
   if inc["category"] not in cats:continue
   km=distance_km(inc["latitude"],inc["longitude"],t["latitude"],t["longitude"]) if inc["latitude"] is not None else None
   suitable.append((t,km))
  if d.get("team_id"):
   suitable=[x for x in suitable if x[0]["id"]==d["team_id"]]
  if not suitable:return json_error("No available suitable team found. Check team category, availability and incident coordinates.",409)
  suitable.sort(key=lambda x:x[1] if x[1] is not None else 0);team,km=suitable[0]
  c.execute("UPDATE teams SET availability='Busy',assigned_incident_id=?,updated_at=? WHERE id=?",(iid,now(),team["id"]))
  c.execute("UPDATE incidents SET assigned_team_id=?,status='Assigned',updated_at=? WHERE id=?",(team["id"],now(),iid))
  c.execute("INSERT INTO assignment_history(incident_id,team_id,action,distance_km,created_at) VALUES(?,?,?,?,?)",(iid,team["id"],"ASSIGNED",km,now()))
 result=one("SELECT i.*,t.name AS assigned_team_name FROM incidents i LEFT JOIN teams t ON t.id=i.assigned_team_id WHERE i.id=?",(iid,))
 return jsonify(item=result,team=one("SELECT * FROM teams WHERE id=?",(team["id"],)),distance_km=km)
@app.get("/api/assignments")
@admin_required
def assignment_history():return jsonify(items=allrows("SELECT h.*,i.title,t.name AS team_name FROM assignment_history h JOIN incidents i ON i.id=h.incident_id JOIN teams t ON t.id=h.team_id ORDER BY h.created_at DESC"))
@app.get("/api/analytics")
def analytics():
 refresh_priorities()
 inc=allrows("SELECT * FROM incidents");teams=allrows("SELECT * FROM teams")
 cats={c:sum(1 for x in inc if x["category"]==c) for c in CATEGORIES}
 return jsonify(total_incidents=len(inc),critical_incidents=sum(x["severity"]=="Critical" for x in inc),
 available_teams=sum(t["availability"]=="Available" for t in teams),busy_teams=sum(t["availability"]=="Busy" for t in teams),
 assigned_incidents=sum(x["status"] in ("Assigned","In Progress") for x in inc),resolved_incidents=sum(x["status"]=="Resolved" for x in inc),
 category_distribution=cats,severity_distribution={s:sum(x["severity"]==s for x in inc) for s in SEVERITIES})
@app.get("/api/map")
def map_data():
 return jsonify(incidents=allrows("SELECT id,title,category,severity,status,latitude,longitude,assigned_team_id FROM incidents WHERE latitude IS NOT NULL AND longitude IS NOT NULL"),
 teams=allrows("SELECT id,name,response_category,availability,latitude,longitude,assigned_incident_id FROM teams"))
@app.post("/api/analyse-image")
def analyse_image():
 f=request.files.get("photo")
 if not f:return json_error("Photo is required.")
 ext=(f.filename.rsplit(".",1)[-1] if "." in f.filename else "").lower()
 if ext not in {"png","jpg","jpeg","webp"}:return json_error("Upload PNG, JPG or WEBP.")
 raw=f.read()
 if len(raw)>8*1024*1024:return json_error("Image exceeds 8 MB.")
 key=os.getenv("OPENAI_API_KEY")
 if not key:return json_error("Photo AI is not configured. Add OPENAI_API_KEY to .env.",503)
 try:
  import requests
  mime=mimetypes.guess_type(secure_filename(f.filename))[0] or "image/jpeg"
  payload={"model":os.getenv("OPENAI_VISION_MODEL","gpt-4.1-mini"),"messages":[{"role":"user","content":[{"type":"text","text":"Inspect this emergency scene photo. Return ONLY JSON with title, description, category, severity. Category must be one of "+", ".join(CATEGORIES)+". Severity one of Low, Medium, High, Critical. Describe visible evidence only. Do not identify people, infer invisible injuries, or claim certainty. If unclear use Other Emergencies and Medium."},{"type":"image_url","image_url":{"url":f"data:{mime};base64,{base64.b64encode(raw).decode()}"}}]}],"temperature":0.1}
  r=requests.post("https://api.openai.com/v1/chat/completions",headers={"Authorization":f"Bearer {key}"},json=payload,timeout=45);r.raise_for_status()
  content=r.json()["choices"][0]["message"]["content"];content=re.sub(r"^```(?:json)?|```$","",content.strip(),flags=re.I).strip();d=json.loads(content)
  if d.get("category") not in CATEGORIES:d["category"]="Other Emergencies"
  if d.get("severity") not in SEVERITIES:d["severity"]="Medium"
  return jsonify({k:str(d.get(k,"")) for k in ["title","description","category","severity"]})
 except Exception as e:return json_error("Photo analysis failed: "+type(e).__name__,502)
@app.errorhandler(413)
def too_large(e):return json_error("Uploaded file is too large (8 MB maximum).",413)
if __name__=="__main__":
 init_db()
 import webbrowser, threading
 if os.getenv("AEGIS_NO_BROWSER")!="1":threading.Timer(1.2,lambda:webbrowser.open("http://127.0.0.1:5000/")).start()
 app.run(host="127.0.0.1",port=int(os.getenv("PORT","5000")),debug=False)

init_db()

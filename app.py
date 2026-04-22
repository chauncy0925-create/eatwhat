from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users":{},"groups":{},"orders":[]}
    with open(DB_FILE,"r",encoding="utf-8") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f:
        json.dump(db,f,ensure_ascii=False)

# 菜单
@app.route("/add", methods=["POST"])
def add():
    d = request.get_json()
    db = load_db()
    u = d["user"]
    if u not in db["users"]:db["users"][u]={"food":[]}
    db["users"][u]["food"].append({"name":d["name"]})
    save_db(db)
    return "ok"

@app.route("/food")
def food():
    u = request.args.get("user")
    db = load_db()
    return jsonify(db["users"].get(u,{"food":[]})["food"])

# 订单
@app.route("/order",methods=["POST"])
def order():
    d = request.get_json()
    db=load_db()
    db["orders"].append(d)
    save_db(db)
    return "ok"

# 群组
@app.route("/create_group",methods=["POST"])
def cg():
    d=request.get_json()
    db=load_db()
    gid = str(len(db["groups"])+1)
    db["groups"][gid]={"name":d["name"],"owner":d["owner"],"foods":[],"orders":[]}
    save_db(db)
    return jsonify({"id":gid})

@app.route("/group")
def gg():
    db=load_db()
    return jsonify(db["groups"].get(request.args.get("id"),{}))

@app.route("/group_food",methods=["POST"])
def gfood():
    d=request.get_json()
    db=load_db()
    g=db["groups"][d["gid"]]
    if g["owner"]!=d["owner"]:return "no"
    g["foods"].append(d["name"])
    save_db(db)
    return "ok"

@app.route("/group_order",methods=["POST"])
def go():
    d=request.get_json()
    db=load_db()
    g=db["groups"][d["gid"]]
    g["orders"].append({"user":d["user"],"list":d["list"]})
    save_db(db)
    return "ok"

@app.route("/group_summary")
def gs():
    db=load_db()
    g=db["groups"].get(request.args.get("id"),{"orders":[]})
    return jsonify(g["orders"])

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)

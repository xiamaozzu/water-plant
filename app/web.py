"""Flask Web 服务"""
from flask import Flask, render_template, request, redirect, url_for, flash
from . import db

app = Flask(__name__)
app.secret_key = "water-plant-dev-secret"


@app.route("/", methods=["GET"])
def index():
    records = []
    try:
        records = db.list_test(limit=10)
    except Exception as e:
        flash(f"读取数据库失败：{e}")
    return render_template("index.html", records=records)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip()
    content = request.form.get("content", "").strip()
    if not name or not content:
        flash("名称和内容都不能为空")
        return redirect(url_for("index"))
    try:
        new_id = db.insert_test(name, content)
        flash(f"写入成功！新记录 id={new_id}")
    except Exception as e:
        flash(f"写入失败：{e}")
    return redirect(url_for("index"))

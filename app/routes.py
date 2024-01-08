from app import app, executor
from app.models import get_latest_ratings, store_latest_ratings
from lib import rym
from flask import render_template, request


@app.route("/")
@app.route("/index")
def index():
    groups = get_latest_ratings("timestamp")
    return render_template("index.html", groups=groups)

@app.route("/ratings")
@app.route("/ratings/<order_by>")
def ratings(order_by=None):
    groups = get_latest_ratings(order_by or request.args.get("order_by", "timestamp"))
    return render_template("ratings.html", groups=groups)

@app.route("/update")
def update():
    executor.submit(store_latest_ratings)
    return "Ratings update queued"
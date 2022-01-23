from datetime import datetime, timedelta
import os

from flask import Flask, make_response, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route("/zara")
def zara():
    return render_template('index.html')

@app.route("/")
def home():
    return redirect(url_for("zara"))


@app.route("/favicon.ico")
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))


def check_credentials(username, password):
    checked = False
    if username is not None and password is not None:
        username = username.strip().lower().replace(" ", "")
        password = password.strip().lower().replace(" ", "")
        if os.environ.get("PRESENT_USR") == username and os.environ.get("PRESENT_PASS") == password:
            checked = True
    return username, password, checked


@app.route("/present", methods=['GET', 'POST'])
def form():
    username, password, checked = check_credentials(
        request.cookies.get('present_username'), request.cookies.get('present_pass')
    )
    cookies_set = checked
    error = None
    if request.method == "POST":
        username, password, checked = check_credentials(
            request.form["username"], request.form["password"]
        )
        if not checked:
            error = "Invalid credentials"
    resp = make_response(render_template("form.html", checked=checked, error=error))

    if checked and not cookies_set:
        timeout = datetime.now() + timedelta(seconds=60*60*24)
        resp.set_cookie('present_username', username, expires=timeout)
        resp.set_cookie('present_pass', password, expires=timeout)
    return resp

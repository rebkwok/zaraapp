from flask import Flask, render_template

app = Flask(__name__)

@app.route("/zara")
def home():
    return render_template('index.html')

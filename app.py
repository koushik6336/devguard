from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", active="home")

@app.route("/login")
def login():
    return render_template("login.html", active="login")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", active="dashboard")

@app.route("/about")
def about():
    return render_template("about.html", active="about")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

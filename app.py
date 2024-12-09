import os
import dotenv
import time
import secrets
from pathlib import Path
from flask import *
import sys
import json
import random
from hashlib import sha256

sys.path.append(str(Path(__file__).resolve().parent))

root_dir = Path(os.getcwd())
static_dir = root_dir / 'static'

dotenv.load_dotenv(root_dir / '.env')

app = Flask(__name__)
app.secret_key = os.getenv("SUPER_SECRETE_KEY") if os.getenv(
    "SUPER_SECRETE_KEY") else secrets.token_hex(16)


print(f"Current working directory: {os.getcwd()}")
print(f"PRESETS_PATH: {os.getenv('PRESETS_PATH')}")

users: dict[str] = json.loads(os.getenv("USERS")) if os.getenv("USERS") else {}
devices: dict[str] = json.loads(
    os.getenv("DEVICES")) if os.getenv("DEVICES") else {}

with open(Path(os.getcwd()) / Path(os.getenv("PRESETS_PATH").strip('"'))) as r:
    presets = json.load(r)

with open(Path(os.getcwd()) / Path(os.getenv("UTILS_PATH").strip('"'))) as r:
    utils = json.load(r)


def analyzediseasehandler(username: str, device: str):
    time.sleep(1)
    return utils[random.randint(0, len(utils)-1)]


def strhashcode(s: str):
    return sha256(s.encode('utf-8')).hexdigest()


@app.route("/", methods=["GET", "POST"])
def index():
    if "username" in session:
        username = session["username"]
        return f"Hello, {username}! <br><a href='/logout'>Logout</a>", 200
    else:
        return "You are not logged in. <br><a href='/login'>Login</a>", 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username")
        password = strhashcode(request.form.get("password"))
        print(username)
        print(password)

        if username in users and users[username] == password:
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("index")), 302

        flash("Invalid credentials. Please try again.", "danger")
        return render_template("login.html"), 401

    return render_template("login.html"), 200


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for('index')), 302


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "username" in session:
        return redirect(url_for("index")), 302

    if request.method == "POST":
        username = request.form.get("username")
        password = strhashcode(request.form.get("password"))

        if len(username) < 3 or len(password) < 4:
            flash(
                "Username must be at least 3 characters and password at least 4 characters.", "danger")
            return render_template("login.html"), 400

        if not username or not password:
            flash("Username and password are required.", "danger")
            return render_template("signup.html")

        if username not in users:
            users[username] = password
            flash("Sign Up successful! Please log in.", "success")
            return redirect(url_for("login")), 302
        else:
            flash("Username already exists. Please choose a different one.", "danger")

    return render_template("signup.html"), 200


@app.route('/forgotmypw', methods=['GET'])
def forgotmypw():
    if "username" in session:
        return redirect(url_for("index")), 302

    return render_template("forgotmypw.html"), 200


@app.route('/registerdevice', methods=['GET', 'POST'])
def registerdevice():
    if "username" not in session:
        return redirect(url_for("login")), 302

    if request.method == "POST":
        devicecode = request.form.get("devicecode")
        print(devicecode)
        if not devicecode:
            return jsonify({'message': 'Device Code is required.'}), 400

        username = session["username"]

        if username not in devices.keys() or devicecode not in devices[username]:
            devices[username].append(devicecode)
            flash('Successfully registered', 'message')
            return redirect(url_for("listdevice")), 302
        else:
            flash('Already registered device', 'message')
            return redirect(url_for("registerdevice")), 302
    return render_template("registerdevice.html"), 200


@app.route('/listdevice', methods=['GET'])
def listdevice():
    if "username" not in session:
        return redirect(url_for("login")), 302
    username = session["username"]
    if username not in devices.keys():
        return jsonify({'status': 200, 'message': 'No devices detected', 'data': {'devices': []}}), 200
    return jsonify({'status': 200, 'message': 'Successfully loaded your devices', 'data': {'devices': devices[username]}}), 200


@app.route('/analyzedisease/<string:device>', methods=['GET'])
def analyzedisease(device: str):
    if "username" not in session:
        return redirect(url_for("login")), 302
    username = session["username"]
    if username not in devices.keys() or device not in devices[username]:
        return jsonify({'status': 200, 'message': 'No devices detected', 'data': {'devices': []}}), 200
    result = analyzediseasehandler(username, device)
    return jsonify({'status': 200, 'message': 'Successfully loaded your devices', 'data': {'result': result}}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8000)

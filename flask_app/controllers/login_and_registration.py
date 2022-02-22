from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("login_and_registration.html")


@app.route("/new_user", methods=['POST'])
def new_user():
    if not User.validate_user(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "gender": request.form["gender"],
        "email": request.form["email"],
        "password" : pw_hash,
    }
    user_id = User.create_user(data)
    session['user_first_name'] = data["first_name"]
    session['loged_in'] = True
    return redirect ("/dashboard")


@app.route("/login", methods=['POST'])
def login():
    data = request.form
    results = User.login(data)
    if not results:
        flash("Invalid Email/Password!",'login')
        return redirect("/")
    if not bcrypt.check_password_hash(results.password, request.form['password']):
        flash("Invalid Email/Password!", 'login')
        return redirect('/')
    session['user_first_name'] = results.first_name
    session['loged_in'] = True
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if not "loged_in" in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/clear_session", methods=["POST"])
def clear_session():
    session.clear()
    return redirect("/")

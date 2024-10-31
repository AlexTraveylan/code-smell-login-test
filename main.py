from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = "votre_clé_secrète_ici"  # Important pour la session

# Simuler une base de données d'utilisateurs (dans un vrai projet, utilisez une vraie BD)
users = {"admin": "password123"}

# Code smell volantaire pour voir si c'est detecté
global_var = "foo"


def code_smell():
    try:
        f = open("noexist.txt")
        print(global_var)
    except:
        print("nto exist")
    finally:
        f.close()


# Fin du code smell volontaire


# Décorateur pour protéger les routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Veuillez vous connecter pour accéder à cette page")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            flash("Connexion réussie!")
            return redirect(url_for("protected"))
        else:
            flash("Identifiants incorrects")

    return render_template("login.html")


@app.route("/protected")
@login_required
def protected():
    return render_template("protected.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Vous êtes déconnecté")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

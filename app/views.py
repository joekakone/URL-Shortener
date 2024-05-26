#!/usr/bin/env python
# coding : utf-8

"""
    Flask CHallenge #03 : Authentification
"""

import datetime
import urllib

from flask import render_template, request, url_for, redirect, session, flash
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, bcrypt
from app.models import User, Url
from app.utils import transform_url

@app.route("/")
def index():
    urls = Url.query.all()
    return render_template("index.html", urls=urls)

# Create
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("profile", id=current_user.id))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(username=username,
                    email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("profile", id=user.id))

    return render_template("signup.html")

@app.route("/profile/<int:id>", methods=["GET", "POST"])
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template("profile.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        print(current_user.id)
        return redirect(url_for("profile", id=current_user.id))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter(User.email == email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for("profile", id=user.id))

        # return redirect(url_for("index"))
        flash("Invalid Credentails !")

    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()

    return redirect(url_for("login"))

# Urls : C.R.U.D
# Create
@app.route("/url/create", methods=["GET", "POST"])
@login_required
def create_url():
    if request.method == "POST":
        name = request.form.get("name")
        input_url = request.form.get("url")

        # Create URL item in database
        url = Url(name=name,
                  long_url=input_url,
                  created_date=datetime.datetime.now(),
                  user_id=current_user.id)
        db.session.add(url)
        db.session.commit()

        # Create the short URL
        output_url = transform_url(url.id)
        url.short_url = output_url
        print()
        db.session.commit()

        return redirect(url_for("view_url", id=url.id))

    return render_template("create_url.html")

# Read
@app.route("/url/<int:id>/details", methods=["GET"])
@login_required
def view_url(id):
    url = Url.query.get_or_404(id)

    return render_template("view_url.html", url=url)

# Update
@app.route("/url/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_url(id):
    url = Url.query.get_or_404(id)

    if request.method == "POST":
        url.name = request.form.get("name")
        url.long_url = request.form.get("url")
        db.session.commit()

        return redirect(url_for("view_url", id=url.id))

    return render_template("update_url.html", url=url)

# Delete
@app.route("/url/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_url(id):
    url = Url.query.get_or_404(id)
    db.session.delete(url)
    db.session.commit()

    return redirect(url_for("index"))


@app.route('/previous_page')
def previous_page():
    # Get the URL of the previous page that the user visited from the session
    previous_page_url = session.get('previous_page_url')

    if previous_page_url:
        # Clear the previous_page_url from the session to prevent repeated redirection
        session.pop('previous_page_url', None)

        # Redirect the user back to the previous page
        return redirect(previous_page_url)
    else:
        # If previous_page_url is not available in the session, redirect to a fallback URL
        return redirect(url_for('index'))


# Redirection
@app.route("/redirect/<string:hashid>", methods=["GET"])
@login_required
def redirection(hashid):
    url = urllib.parse.urljoin(app.config["BASE_URL"], hashid)
    url = Url.query.filter(Url.short_url == url).first()

    return redirect(url.long_url)

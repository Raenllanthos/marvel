from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel_inventory.models import User, Hero, db, check_password_hash
from marvel_inventory.forms import UserLoginForm, HeroForm
from flask_login import login_user, logout_user, login_required

auth = Blueprint("auth", __name__, template_folder="auth_templates")
# api = Blueprint("api", __name__, url_prefix="/api")

@auth.route("/signup", methods = ['GET', 'POST'])
# get gets data from our database, post means they can post on page; methods work universally
# GET/POST/PUT/DELETE are HTTP verbs that describe what we want to do at a given endpoint (location)
def signup():
    form = UserLoginForm()

    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            print(email, username, password)

            user = User(email, username = username, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a user account, {username}", "user-created")

            return redirect(url_for('site.index'))
    except:
        raise Exception("Invalid Form Data: Please Check your form")
    return render_template("signup.html", form=form)

@auth.route("/signin", methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            print(email, username, password)

            logged_user = User.query.filter(User.email == email).first()

            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("You were successfullt loggin in: via Email/Password", "auth-success")
                return redirect(url_for("site.profile"))
            else:
                flash("Your Email/Password is incorrect! Try Again!", "auth-failed")
                return redirect(url_for("auth.signin"))
    except:
        raise Exception("Invalid Form Data: Please Check Your Form!")
    return render_template("signin.html", form=form)

@auth.route("/hero", methods = ['GET', 'POST'])
def hero():
    form = HeroForm()

    try:
        if request.method == "POST" and form.validate_on_submit():
            name = form.name.data
            power = form.power.data
            is_a_hero = form.is_a_hero.data
            comics_appeared_in = form.comics_appeared_in.data
            description = form.description.data
            back_story = form.back_story.data
            print(name, power, comics_appeared_in, description, back_story)

            hero = Hero(name, power, is_a_hero, comics_appeared_in, description, back_story)

            db.session.add(hero)
            db.session.commit()

            flash(f"You have successfully created a hero, {name}", "user-created")

            return redirect(url_for('auth.hero'))
    except:
        raise Exception("Invalid Form Data: Please Check your form")
    return render_template("hero.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("site.index"))
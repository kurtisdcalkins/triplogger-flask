import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from triplog import app, db, bcrypt
from triplog.forms import RegistrationForm, LoginForm, UpdateAccountForm, TripForm
from triplog.models import User, Trip
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/home")
def home():
    trips = Trip.query.all()
    return render_template('home.html', trips=trips)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You may now log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check email and password", 'danger')
    return render_template('login.html', title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' +
                         current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/trip/new", methods=["GET", "POST"])
@login_required
def new_trip():
    form = TripForm()
    if form.validate_on_submit():
        trip = Trip(title=form.title.data, trip_date=form.trip_date.data, difficulty=form.difficulty.data,
                    fun_rating=form.fun_rating.data, trip_group=form.trip_group.data, highlights=form.highlights.data, author=current_user)
        db.session.add(trip)
        db.session.commit()
        flash("The trip has been added!", 'success')
        return redirect(url_for('home'))
    return render_template('create_trip.html', title='New Trip', form=form, legend='+ Add Trip')


@app.route("/trip/<int:trip_id>")
def trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return render_template('trip.html', title=trip.title, trip=trip)


@app.route("/trip/<int:trip_id>/update", methods=["GET", "POST"])
@login_required
def update_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.author != current_user:
        abort(403)
    form = TripForm()
    if form.validate_on_submit():
        trip.title = form.title.data
        trip.trip_date = form.trip_date.data
        trip.difficulty = form.difficulty.data
        trip.fun_rating = form.fun_rating.data
        trip.trip_group = form.trip_group.data
        trip.highlights = form.highlights.data
        db.session.commit()
        flash("Your trip has been updated", 'success')
        return redirect(url_for('trip', trip_id=trip_id))
    elif request.method == 'GET':
        form.title.data = trip.title
        form.trip_date.data = trip.trip_date
        form.difficulty.data = trip.difficulty
        form.fun_rating.data = trip.fun_rating
        form.trip_group.data = trip.trip_group
        form.highlights .data = trip.highlights
    return render_template('create_trip.html', title='Update Trip', form=form, legend='Update Trip')


@app.route("/trip/<int:trip_id>/delete", methods=["POST"])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.author != current_user:
        abort(403)
    db.session.delete(trip)
    db.session.commit()
    flash("Your trip has been deleted.")
    return redirect(url_for('home'))

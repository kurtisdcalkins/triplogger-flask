from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from triplog.models import Trip
from triplog import db
from triplog.trips.forms import TripForm

trips = Blueprint('trips', __name__)


@trips.route("/trip/new", methods=["GET", "POST"])
@login_required
def new_trip():
    form = TripForm()
    if form.validate_on_submit():
        trip = Trip(title=form.title.data, trip_date=form.trip_date.data, difficulty=form.difficulty.data,
                    fun_rating=form.fun_rating.data, trip_group=form.trip_group.data, highlights=form.highlights.data, author=current_user)
        db.session.add(trip)
        db.session.commit()
        flash("The trip has been added!", 'success')
        return redirect(url_for('main.home'))
    return render_template('create_trip.html', title='New Trip', form=form, legend='+ Add Trip')


@trips.route("/trip/<int:trip_id>")
def trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return render_template('trip.html', title=trip.title, trip=trip)


@trips.route("/trip/<int:trip_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for('trips.trip', trip_id=trip_id))
    elif request.method == 'GET':
        form.title.data = trip.title
        form.trip_date.data = trip.trip_date
        form.difficulty.data = trip.difficulty
        form.fun_rating.data = trip.fun_rating
        form.trip_group.data = trip.trip_group
        form.highlights .data = trip.highlights
    return render_template('create_trip.html', title='Update Trip', form=form, legend='Update Trip')


@trips.route("/trip/<int:trip_id>/delete", methods=["POST"])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.author != current_user:
        abort(403)
    db.session.delete(trip)
    db.session.commit()
    flash("Your trip has been deleted.")
    return redirect(url_for('main.home'))


# Add routes for filtering the trips
# @trips.route("/filter/<date>")
# def filter_year(year):
#     trips = Trip.query.filter_by(year)
#     return render_template('new_template.html', trips=trips)

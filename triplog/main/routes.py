from flask import render_template, request, Blueprint
from triplog.models import Trip

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template('index.html')


@main.route("/home")
def home():
    trips = Trip.query.order_by(Trip.trip_date.desc())
    return render_template('home.html', trips=trips)

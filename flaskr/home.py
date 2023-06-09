import base64
from io import BytesIO
from matplotlib.figure import Figure
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.weather_api import current_temp
from flaskr.db import Plants, FlowerPot, Measurements
from flaskr.api_measurements import get_measurement_api

bp = Blueprint("home", __name__)


@bp.route("/")
@login_required
def index():
    db = get_db()
    status = "All Good"
    plants_list = Plants.query.order_by(Plants.id.desc()).all()
    flower_pots = FlowerPot.query.order_by(FlowerPot.id.desc()).all()
    soil_moisture = (
        Measurements.query.order_by(Measurements.id.desc()).first().soil_moisture
    )  # fetch latest soil moisture

    for pot in flower_pots:
        flower_moist_needed = (
            Plants.query.filter_by(name=pot.plant).first().soil_moisture
        )
        if soil_moisture < flower_moist_needed:
            status = "Water the Plants"
        else:
            status = "All Good"
        pot.status = status
        db.commit()

    return render_template(
        "home/index.html",
        flower_pots=flower_pots,
        plants_list=plants_list,
        soil_moisture=soil_moisture,
    )


@bp.route("/create", methods=("GET", "POST"))
@login_required  # login required to create
def create():
    """Creating a new flower pot"""
    db = get_db()
    plants_list = Plants.query.order_by(Plants.id.desc()).all()
    if request.method == "POST":
        pot_name = request.form["title"]
        plant = request.form.get("plant_select")
        error = None

        if not pot_name:
            error = "Pot name is required."
        elif not plant:
            error = "Plant name is required."

        if error is not None:
            flash(error)
        else:
            new_pot = FlowerPot(pot_name=pot_name, plant=plant)
            db.add(new_pot)
            db.commit()
            return redirect(
                url_for("home.index")
            )  # redirecting back to home page after successful create

    return render_template("home/create.html", plants_list=plants_list)


def get_pot(id):
    """Get pot id"""
    db = get_db()
    pot = db.query(FlowerPot).filter_by(id=id).first()

    if pot is None:
        abort(404, f"Pot id {id} doesn't exist.")
    return pot


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update already created flower pot"""
    pot = get_pot(id)
    db = get_db()
    plants_list = Plants.query.order_by(Plants.id.desc()).all()
    if request.method == "POST":
        pot_name = request.form["title"]
        plant = request.form.get("plant_select")
        error = None

        if not pot_name:
            error = "Pot name is required."
        elif not plant:
            error = "Plant name is required."

        if error is not None:
            flash(error)
        else:
            pot.pot_name = pot_name
            pot.plant = plant
            db.commit()
            return redirect(url_for("home.index"))

    return render_template("home/update.html", pot=pot, plants_list=plants_list)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delet a flower pot"""
    get_pot(id)
    db = get_db()
    pot = FlowerPot.query.get(id)
    db.delete(pot)
    db.commit()
    return redirect(url_for("home.index"))


@bp.route("/<int:id>/details", methods=("GET", "POST"))
@login_required
def details(id):
    """
    Details of a flower pot
    """
    try:
        """
        Using try so the app executes normally,
        if the other docker that is providing the measurements is not up
        """
        db = get_db()
        new_measurement = Measurements(
            soil_moisture=get_measurement_api("soil_moisture"),
            acidity=get_measurement_api("acidity"),
            lux=get_measurement_api("lux"),
        )
        db.add(new_measurement)
        db.commit()
    except:
        print("Connection to the new measurements is broke")
    pot = FlowerPot.query.get(id)
    plants_list = Plants.query.order_by(Plants.id.desc()).all()
    measurements = Measurements.query.order_by(Measurements.id).all()
    soil_moisture = []
    acidity = []
    lux = []
    for row in measurements:
        soil_moisture.append(row.soil_moisture)
        acidity.append(row.acidity)
        lux.append(row.lux)
    last_sensor_measurements = Measurements.query.order_by(
        Measurements.id.desc()
    ).first()
    lux = list(map(lambda x: x // 10, lux))  # scale lux by 10
    # Generate the figure **without using pyplot**.Based on the post button
    if request.method == "POST":
        # generate plot based on button click
        if request.form.get("pie"):
            # pie chart
            fig = Figure()
            ax = fig.subplots()
            ax.pie(
                [sum(soil_moisture), sum(acidity), sum(lux)],
                labels=["soil_moisture", "acidity", "lux"],
            )
        elif request.form.get("histo"):
            # histogram
            fig = Figure()
            ax = fig.subplots()
            ax.hist(soil_moisture, alpha=0.5, label="soil_moisture")
            ax.hist(acidity, alpha=0.5, label="acidity")
            ax.hist(lux, alpha=0.5, label="lux")
            ax.legend(loc="upper right")
        else:
            # line plot (default)
            fig = Figure()
            ax = fig.subplots()
            ax.plot(soil_moisture)
            ax.plot(acidity)
            ax.plot(lux)
    else:
        # default line plot
        fig = Figure()
        ax = fig.subplots()
        ax.plot(soil_moisture)
        ax.plot(acidity)
        ax.plot(lux)
    # Save it to a temporary buffer.)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return render_template(
        "home/details.html",
        sensor_measurement=last_sensor_measurements,
        pot=pot,
        plants_list=plants_list,
        data=data,
        current_temp=current_temp,
    )

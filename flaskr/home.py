import base64
from io import BytesIO
from matplotlib.figure import Figure
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.weather_api import current_temp

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required
def index():
    '''Fetching data stored for certain flower pot to be displayed'''
    db = get_db()
    plants_list = db.execute('SELECT * FROM plants ORDER by id DESC').fetchall()
    flower_pots = db.execute(
        ' SELECT id, pot_name, plant'
        ' FROM flower_pot'
        ' ORDER BY id DESC'
    ).fetchall()
    soil_moisture = db.execute('SELECT soil_moisture FROM measurements ORDER by id DESC').fetchone() #fetch latest soil moisture
    return render_template('home/index.html',flower_pots = flower_pots, plants_list = plants_list, soil_moisture = soil_moisture)

@bp.route('/create', methods=('GET', 'POST'))
@login_required #login required to create
def create():
    '''Creating a new flower pot'''
    db = get_db()
    plants_list = db.execute('SELECT * FROM plants ORDER by id DESC').fetchall()
    if request.method == 'POST':
        pot_name = request.form['title']
        plant = request.form.get('plant_select')
        error = None

        if not pot_name:
            error = 'Pot name is required.'
        elif not plant:
            error = 'Plant name is required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO flower_pot (pot_name, plant)'
                ' VALUES (?, ?)',
                (pot_name, plant)
            )
            db.commit()
            return redirect(url_for('home.index')) #redirecting back to home page after successful create

    return render_template('home/create.html', plants_list=plants_list)

def get_pot(id):
    '''Get pot id '''
    db = get_db()
    pot = db.execute(
        'SELECT *FROM flower_pot WHERE id = ?',
        (id,)
    ).fetchone()

    if pot is None:
        abort(404, f"Pot id {id} doesn't exist.")
    return pot

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    '''Update already created flower pot'''
    pot = get_pot(id)
    db = get_db()
    plants_list = db.execute('SELECT * FROM plants ORDER by id DESC').fetchall()
    if request.method == 'POST':
        pot_name = request.form['title']
        plant = request.form.get('plant_select')
        error = None

        if not pot_name:
            error = 'Pot name is required.'
        elif not plant:
            error = 'Plant name is required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                ' UPDATE flower_pot SET pot_name = ?, plant = ?'
                ' WHERE id = ?',
                (pot_name, plant, id)
            )
            db.commit()
            return redirect(url_for('home.index'))

    return render_template('home/update.html', pot=pot, plants_list=plants_list)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    '''Delet a flower pot'''
    get_pot(id)
    db = get_db()
    db.execute('DELETE FROM flower_pot WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('home.index'))

@bp.route('/<int:id>/details',methods=('GET','POST'))
@login_required
def details(id):
    '''
    Details of a flower pot
    '''
    pot = get_pot(id)
    db = get_db()
    
    plants_list = db.execute('SELECT * FROM plants ORDER by id DESC').fetchall()
    measurements = db.execute('SELECT * FROM measurements ORDER by id').fetchall()
    soil_moisture = []
    acidity = []
    lux = []
    for row in measurements:
        soil_moisture.append(row[1])
        acidity.append(row[2])
        lux.append(row[3])
    last_sensor_measurements = db.execute('SELECT * FROM measurements ORDER by id DESC').fetchone()
    lux = list(map(lambda x: x//10, lux)) # scale lux by 10
    # Generate the figure **without using pyplot**.Based on the post button
    if request.method == 'POST':
        # generate plot based on button click
        if request.form.get('pie'):
            # pie chart
            fig = Figure()
            ax = fig.subplots()
            ax.pie([sum(soil_moisture), sum(acidity), sum(lux)], labels=['soil_moisture', 'acidity', 'lux'])
        elif request.form.get('histo'):
            # histogram
            fig = Figure()
            ax = fig.subplots()
            ax.hist(soil_moisture, alpha=0.5, label='soil_moisture')
            ax.hist(acidity, alpha=0.5, label='acidity')
            ax.hist(lux, alpha=0.5, label='lux')
            ax.legend(loc='upper right')
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

    return render_template('home/details.html',
                           sensor_measurement = last_sensor_measurements, pot = pot,
                             plants_list=plants_list, data=data, current_temp= current_temp)




from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import base64

bp = Blueprint('plants', __name__)

@bp.route('/plants')
@login_required
def index():
    '''
    Fetching flowers data to be displayed
    '''
    db = get_db()
    plants = db.execute('SELECT * FROM plants ORDER by id DESC').fetchall()
    return render_template('plants/index.html', plants = plants)

@bp.route('/plants/create',methods=('GET', 'POST'))
@login_required
def create():
    '''
    Create new Flower
    '''
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        #converting uploaded image to blob, and encode
        image = request.files['image'].read()
        image_blob = base64.b64encode(image)

        humidity = request.form['humidity']
        light = request.form['light']
        substrate = request.form['substrate']
        error = None

        if not name:
            error = 'Pot name is required'
        elif not image_blob:
            error = 'Image is required'
        elif not humidity:
            error = 'Humiditiy is required'
        elif not light:
            error = 'Light is required'

        if error is not None:
            flash(error)
        else:
            db.execute('INSERT INTO plants (name, image, humidity, light, substrate)'
                       'VALUES (?,?,?,?,?)',
                       (name,image_blob,humidity,light,substrate)
                       )
            db.commit()
            return redirect(url_for('plants.index'))
    return render_template('plants/create.html')

def get_plant(id):
    '''Get pot id '''
    db = get_db()
    plant = db.execute(
        'SELECT *FROM plants WHERE id = ?',
        (id,)
    ).fetchone()

    if plant is None:
        abort(404, f"Plant id {id} doesn't exist.")
    return plant

@bp.route('/plants/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    '''Update already created flower pot'''
    plant = get_plant(id)
    db = get_db()
    plants_list = db.execute('SELECT * FROM plants ORDER by id DESC').fetchall()
    if request.method == 'POST':
        name = request.form['name']
        #converting uploaded image to blob, and encode
        image = request.files['image'].read()
        image_blob = base64.b64encode(image)

        humidity = request.form['humidity']
        light = request.form['light']
        substrate = request.form['substrate']
        error = None

        if not name:
            error = 'Pot name is required'
        #elif not image_blob:
        #    error = 'Image is required'
        elif not humidity:
            error = 'Humiditiy is required'
        elif not light:
            error = 'Light is required'

        if error is not None:
            flash(error)
        else:
            db.execute(
                ' UPDATE plants SET name = ?, image = ?, humidity = ?, light = ?, substrate = ?'
                ' WHERE id = ?',
                (name, image_blob, humidity, light, substrate, id)
            )
            db.commit()
            return redirect(url_for('plants.index'))

    return render_template('plants/update.html', plant=plant, plants_list=plants_list)

@bp.route('/plants/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    '''Delet a plants'''
    get_plant(id)
    db = get_db()
    db.execute('DELETE FROM plants WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('plants.index'))

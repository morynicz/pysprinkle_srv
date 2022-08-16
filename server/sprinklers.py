from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from server.auth import login_required
from server.db import get_db

bp = Blueprint('sprinklers', __name__, url_prefix='/sprinklers')


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    sprinklers = db.execute(
        'SELECT s.id, number, x, y, circuit_id, name'
        ' FROM sprinkler s JOIN circuit c WHERE s.circuit_id = c.id'
        ' ORDER BY s.id ASC'
    ).fetchall()
    if request.method == 'GET':
        return render_template('sprinklers/sprinklers.html', sprinklers=sprinklers)

    if request.method == 'POST':
        number = request.form['number']
        x = request.form['x']
        y = request.form['y']
        circuit_id = request.form['circuit_id']

        print(f"received n:{number} x:{x} y:{y} c:{circuit_id}")

        error = None
        if not number:
            error = "Start not provided"

        if not x:
            error = "X not provided"

        if not y:
            error = "Y id not provided"

        if not circuit_id:
            error = "circuit_id not provided"

        if error is None:
            try:
                db.execute("INSERT INTO sprinkler (number, x, y, circuit_id) VALUES (?,?,?,?)",
                           (number, x, y, circuit_id))
                db.commit()
            except db.IntegrityError:
                error = f"Circuit {circuit_id} does not exist"
            else:
                return redirect(url_for("sprinklers.index"))
        flash(error)

        return redirect(url_for("sprinklers.index"))

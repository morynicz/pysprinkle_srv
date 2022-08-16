from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from server.auth import login_required
from server.db import get_db

bp = Blueprint('circuits', __name__, url_prefix='/circuits')


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    circuits = db.execute(
        'SELECT id, name'
        ' FROM circuit'
        ' ORDER BY id ASC'
    ).fetchall()
    if request.method == 'GET':
        return render_template('circuits/circuits.html', circuits=circuits)

    if request.method == 'POST':
        name = request.form['name']
        number = request.form["number"]

        print(f"received n:{name} nu:{number}")

        error = None
        if not name:
            error = "Name not provided"
        if not number:
            error = "Number not provided"


        if error is None:
            try:
                db.execute("INSERT INTO circuit (name, number) VALUES (?, ?)",
                           (name, number))
                db.commit()
            except db.IntegrityError:
                error = f"Something went wrong"
            else:
                return redirect(url_for("circuits.index"))
        flash(error)

        return redirect(url_for("circuits.index"))

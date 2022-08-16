import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from server.auth import login_required
from server.db import get_db

bp = Blueprint('tasks', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    tasks = db.execute(
        'SELECT t.id, start, duration, circuit_id, name'
        ' FROM task t JOIN circuit c WHERE t.circuit_id = c.id'
        ' ORDER BY start ASC'
    ).fetchall()
    print(tasks)
    if request.method == 'GET':
        print(f"req is {request.headers['Accept']}")
        keys = ["id", "start", "duration", "circuit_id"]
        if 'Accept' in request.headers and "application/json" in request.headers['Accept']:
            return jsonify({
                "current_time": int(time.time()),
                "tasks": [{k: t[k] for k in keys} for t in tasks]
            })
        return render_template('tasks/index.html', tasks=tasks)

    if request.method == 'POST':
        start = request.form['start']
        duration = request.form['duration']
        circuit_id = request.form['circuit_id']

        print(f"received s:{start} d:{duration} c:{circuit_id}")

        error = None
        if not start:
            error = "Start not provided"

        if not duration:
            error = "Duration not provided"

        if not circuit_id:
            error = "Sprinkler id not provided"

        if error is None:
            try:
                db.execute("INSERT INTO task (start, duration, circuit_id) VALUES (?,?,?)",
                           (start, duration, circuit_id))
                db.commit()
            except db.IntegrityError:
                error = f"Sprinkler {circuit_id} does not exist"
            else:
                return redirect(url_for("tasks.index"))
        flash(error)

        return redirect(url_for("tasks.index"))

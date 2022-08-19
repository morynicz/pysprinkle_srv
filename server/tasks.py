import time
from . import tz_manipulation
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
        'SELECT t.id, start, duration, circuit_id, name, number'
        ' FROM task t JOIN circuit c WHERE t.circuit_id = c.id'
        ' ORDER BY start ASC'
    ).fetchall()
    if request.method == 'GET':
        print(f"req is {request.headers['Accept']}")
        if 'Accept' in request.headers and "application/json" in request.headers['Accept']:
            keys = ["id", "start", "duration", "number"]
            return jsonify({
                "current_time": int(time.time()),
                "tasks": [{k: t[k] for k in keys} for t in tasks]
            })
        print(f"woohoo {tasks}")
        converted_tasks = list()
        for task in tasks:
            keys = ["id", "start", "duration", "number", "circuit_id", "name"]
            t = {k: task[k] for k in keys}
            t["start"] = tz_manipulation.utc_to_local(t["start"])
            # print(f"start local: {start} converted  to utc {tz_manipulation.local_to_utc(start)}")
            # print(f"start local: {start} converted to local{tz_manipulation.utc_to_local(start)}")
            converted_tasks.append(t)
        return render_template('tasks/index.html', tasks=converted_tasks)

    if request.method == 'POST':
        start = request.form['start']
        duration = request.form['duration']
        circuit_id = request.form['circuit_id']

        print(f"start local: {start} converted {tz_manipulation.local_to_utc(start)}")

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
                           (tz_manipulation.local_to_utc(start), duration, circuit_id))
                db.commit()
            except db.IntegrityError:
                error = f"Sprinkler {circuit_id} does not exist"
            else:
                return redirect(url_for("tasks.index"))
        flash(error)

        return redirect(url_for("tasks.index"))

    if request.method == 'DELETE':
        print("dupsko")


@bp.route('/task/<int:tid>', methods=('DELETE', 'POST'))
@login_required
def delete(tid):
    db = get_db()
    print(f"deleting task {tid}")
    db.execute("DELETE FROM task WHERE id = ?", (tid,))
    if request.method == 'DELETE':
        print("del req")
        return 200
    return redirect(url_for("tasks.index"))

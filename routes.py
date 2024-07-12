from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app import db
from models import Task

main = Blueprint('main', __name__)


# Your route functions here

@main.route('/profile')
@login_required
def profile():
    amount_added = Task.query.filter_by(added_by=current_user.id).count()
    amount_done = Task.query.filter_by(added_by=current_user.id).filter_by(is_done=True).count()
    percentage = 0
    if amount_done > 0 and amount_added > 0:
        percentage = round(amount_done / amount_added * 100, 2)
    return render_template('profile.html', amount_added=amount_added, amount_done=amount_done, percentage=percentage)


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        task = request.form.get('task')
        new_todo = Task(text=task, added_by=current_user.id)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for('main.index'))
        except:
            return "Error adding task"
    else:
        tasks = Task.query.filter(Task.added_by == current_user.id).filter(Task.is_done == False).order_by(
            Task.date_added.desc()).all()
        return render_template('index.html', tasks_list=tasks)


@main.route('/mark_done/<int:task_id>', methods=['GET'])
@login_required
def mark_done(task_id):
    task = Task.query.get_or_404(task_id)
    try:
        setattr(task, 'is_done', True)
        db.session.commit()
        return redirect(url_for('main.index'))
    except:
        return "Error completing task"

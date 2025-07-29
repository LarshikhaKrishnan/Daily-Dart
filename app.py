# app.py
from flask import Flask, render_template, request, redirect, session,url_for
import csv
from datetime import datetime, date,timedelta
import hashlib
import calendar

app = Flask(__name__)
app.secret_key = 'your_secret_key'
USER_FILE = 'users.csv'
TASK_FILE = 'planner.csv'

# Utility: hash password (simple version)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Read tasks for the logged-in user
def read_tasks(username):
    tasks = []
    try:
        with open(TASK_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    task_name, due_date_str, user = row
                    if user == username:
                        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                        tasks.append({'name': task_name, 'due_date': due_date})
    except FileNotFoundError:
        pass
    return tasks

# Save a new task
def save_task(task, due_date, username):
    with open(TASK_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([task, due_date, username])

# Delete a task
def delete_task(task_name, due_date, username):
    tasks = []
    with open(TASK_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row != [task_name, due_date, username]:
                tasks.append(row)
    with open(TASK_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(tasks)

# User registration
def register_user(username, password):
    with open(USER_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, hash_password(password)])

# Validate user login
def validate_user(username, password):
    try:
        with open(USER_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2 and row[0] == username and row[1] == hash_password(password):
                    return True
    except FileNotFoundError:
        pass
    return False

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return redirect('/calendar')

@app.route('/calendar')
def calendar_view():
    if 'user' not in session:
        return redirect('/login')
    year = int(request.args.get('year', date.today().year))
    month = int(request.args.get('month', date.today().month))
    month_days = calendar.monthcalendar(year, month)
    return render_template('calendar.html', year=year, month=month, month_days=month_days)

@app.route('/day/<day_date>', methods=['GET', 'POST'])
def day_view(day_date):
    if 'user' not in session:
        return redirect('/login')

    target_date = datetime.strptime(day_date, '%Y-%m-%d').date()

    if request.method == 'POST':
        task_text = request.form.get('task')
        if task_text:
            save_task(task_text, day_date, session['user'])
        return redirect(url_for('day_view', day_date=day_date))

    tasks = [t for t in read_tasks(session['user']) if t['due_date'].strftime('%Y-%m-%d') == day_date]

    # 👉 Add prev and next dates
    prev_day = (target_date - timedelta(days=1)).strftime('%Y-%m-%d')
    next_day = (target_date + timedelta(days=1)).strftime('%Y-%m-%d')

    return render_template(
        'day.html',
        tasks=tasks,
        date=day_date,
        prev_day=prev_day,
        next_day=next_day
    )

@app.route('/add', methods=['POST'])
def add_task():
    if 'user' not in session:
        return redirect('/login')

    task = request.form.get('task')
    due_date = request.form.get('due_date')

    if task and due_date:
        save_task(task, due_date, session['user'])

    return redirect(f"/day/{due_date}")

@app.route('/delete', methods=['POST'])
def delete():
    if 'user' not in session:
        return redirect('/login')

    task = request.form.get('task')
    due_date = request.form.get('due_date')

    if task and due_date:
        delete_task(task, due_date, session['user'])

    return redirect(f"/day/{due_date}")

@app.route('/todo')
def todo():
    if 'user' not in session:
        return redirect('/login')
    tasks = read_tasks(session['user'])
    sorted_tasks = sorted(tasks, key=lambda x: x['due_date'])
    return render_template('todo.html', all_tasks=sorted_tasks, today=date.today().strftime('%Y-%m-%d'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_user(username, password):
            session['user'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user(username, password)
        return redirect('/login')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
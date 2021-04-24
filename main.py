from flask import Flask, render_template, redirect, request, abort
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from forms.add_user_form import RegisterForm
from forms.login_form import LoginForm
from forms.jobform import JobForm
from forms.departmentform import DepartmnetForm
from flask_login import LoginManager, login_user, logout_user, login_required, \
    current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
def index():
    session = db_session.create_session()
    jobs = list(session.query(Jobs))
    param = {
        "jobs": jobs,
        "title": 'Work log'
    }
    return render_template("work_log.html", **param)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(
                User.email == form.username.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data,
        user.name = form.name.data,
        user.age = form.age.data,
        user.position = form.position.data,
        user.speciality = form.speciality.data,
        user.address = form.address.data,
        user.email = form.username.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/register')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.collaborators = form.collaborators.data
        job.work_size = form.work_size.data
        job.is_finished = form.is_finished.data
        job.job = form.job.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Adding a job', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         (Jobs.user == current_user) | (
                                                 current_user.id == 1)).first()
        if job:
            form.team_leader.data = job.user.id
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         (Jobs.user == current_user) | (
                                                 current_user.id == 1)).first()
        if job:
            job.team_leader = form.team_leader.data
            job.collaborators = form.collaborators.data
            job.work_size = form.work_size.data
            job.is_finished = form.is_finished.data
            job.job = form.job.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html', title='Edit job', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id,
                                     (Jobs.user == current_user) | (
                                             current_user.id == 1)).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
@login_required
def departments_log():
    session = db_session.create_session()
    departments = list(session.query(Department))
    param = {
        "departments": departments,
        "title": 'List of departments'
    }
    return render_template("department_log.html", **param)


@app.route('/adddepartment', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmnetForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Department()
        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.members = form.members.data
        dep.email = form.email.data
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments')
    return render_template('department.html', title='Adding a Department',
                           form=form)


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id, (
            Department.user == current_user) | (current_user.id == 1)).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmnetForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id, (
                Department.user == current_user) | (
                                                       current_user.id == 1)).first()
        if dep:
            form.title.data = dep.title
            form.email.data = dep.email
            form.chief.data = dep.chief
            form.members.data = dep.members
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id, (
                Department.user == current_user) | (
                                                       current_user.id == 1)).first()
        if dep:
            dep.title = form.title.data
            dep.email = form.email.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('department.html', title='Edit department',
                           form=form)


if __name__ == '__main__':
    main()

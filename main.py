from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
def index():
    session = db_session.create_session()
    jobs = list(session.query(Jobs))
    param = {
        "jobs": jobs
    }
    return render_template("works.html", **param)


if __name__ == '__main__':
    main()

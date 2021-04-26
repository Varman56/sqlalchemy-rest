from flask_restful import Resource, abort
from data import db_session
from data.jobs import Jobs
from data.category import Category
from flask import jsonify
from data.jobs_parser import *


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).get(jobs_id)
        return jsonify(
            {
                'jobs': jobs.to_dict(
                    only=(
                        'id', 'team_leader', 'job', 'work_size',
                        'collaborators',
                        'start_date', 'end_date', 'is_finished'))
            }
        )

    def delete(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(jobs_id)
        db_sess.delete(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        args = edit_pasres.parse_args()
        db_sess = db_session.create_session()
        cats = args['categories']
        cat = db_sess.query(Category).filter(Category.name == cats).first()
        if not cat:
            cat = Category()
            cat.name = cats
            db_sess.add(cat)
            db_sess.commit()
            cat = db_sess.query(Category).filter(Category.name == cats).first()
        job = db_sess.query(Jobs).get(jobs_id)
        job.categories = [cat]
        job.team_leader = args['team_leader']
        job.collaborators = args['collaborators']
        job.work_size = args['work_size']
        job.is_finished = args['is_finished']
        job.job = args['job']
        db_sess.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return jsonify(
            {
                'jobs':
                    [item.to_dict(only=(
                        'id', 'team_leader', 'job', 'work_size',
                        'collaborators',
                        'start_date', 'end_date', 'is_finished'))
                        for item in jobs]
            }
        )

    def post(self):
        args = add_parser.parse_args()
        db_sess = db_session.create_session()
        cats = args['categories']
        cat = db_sess.query(Category).filter(Category.name == cats).first()
        if not cat:
            cat = Category()
            cat.name = cats
            db_sess.add(cat)
            db_sess.commit()
            cat = db_sess.query(Category).filter(Category.name == cats).first()
        job = Jobs(
            id=args['id'],
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],

        )
        job.categories.append(cat)
        db_sess.add(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})

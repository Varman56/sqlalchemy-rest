import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs
from .category import Category

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=(
                    'id', 'team_leader', 'job', 'work_size', 'collaborators',
                    'start_date', 'end_date', 'is_finished'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(
                only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                      'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators',
                  'is_finished', 'categories']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first()
    if job:
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],

    )
    cats = request.json['categories']
    cat = db_sess.query(Category).filter(Category.name == cats).first()
    if not cat:
        cat = Category()
        cat.name = cats
        db_sess.add(cat)
        db_sess.commit()
        cat = db_sess.query(Category).filter(Category.name == cats).first()
    job.categories.append(cat)
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_jobs(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators',
                  'is_finished', 'categories']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if not job:
        return jsonify({'error': f'No job with id = {jobs_id}'})
    cats = request.json['categories']
    cat = db_sess.query(Category).filter(Category.name == cats).first()
    if not cat:
        cat = Category()
        cat.name = cats
        db_sess.add(cat)
        db_sess.commit()
        cat = db_sess.query(Category).filter(Category.name == cats).first()
    job.categories = [cat]
    job.team_leader = request.json['team_leader']
    job.collaborators = request.json['collaborators']
    job.work_size = request.json['work_size']
    job.is_finished = request.json['is_finished']
    job.job = request.json['job']
    db_sess.commit()
    return jsonify({'success': 'OK'})

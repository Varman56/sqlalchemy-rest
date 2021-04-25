import flask
from flask import jsonify, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=(
                    'id', 'surname', 'name', 'age', 'city_from', 'position',
                    'speciality', 'address', 'email', 'hashed_password',
                    'modified_date'))
                    for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': user.to_dict(
                only=('id', 'surname', 'name', 'age', 'position', 'city_from',
                      'speciality', 'address', 'email', 'hashed_password',
                      'modified_date'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 'city_from',
                  'speciality', 'address', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == request.json['id']).first()
    if user:
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        city_from=request.json['city_from'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'])
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_users(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'city_from',
                  'speciality', 'address', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': f'No job with id = {user_id}'})
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    user.city_from = request.json['city_from']
    user.set_password(request.json['password'])
    db_sess.commit()
    return jsonify({'success': 'OK'})

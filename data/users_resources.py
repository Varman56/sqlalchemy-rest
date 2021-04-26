from flask_restful import Resource, abort
from data import db_session
from data.users import User
from flask import jsonify
from data.users_parser import *


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {
                'users': user.to_dict(
                    only=(
                        'id', 'surname', 'name', 'age', 'position',
                        'city_from',
                        'speciality', 'address', 'email', 'hashed_password',
                        'modified_date'))
            }
        )

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = edit_pasres.parse_args()
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        user.city_from = args['city_from']
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.set_password(args['password'])
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'users':
                    [item.to_dict(only=(
                        'id', 'surname', 'name', 'age', 'city_from',
                        'position',
                        'speciality', 'address', 'email', 'hashed_password',
                        'modified_date'))
                        for item in users]
            }
        )

    def post(self):
        args = add_parser.parse_args()
        session = db_session.create_session()
        user = User(
            id=args['id'],
            city_from=args['city_from'],
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'])
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

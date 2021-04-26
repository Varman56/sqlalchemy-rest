from flask_restful import reqparse

add_parser = reqparse.RequestParser()
add_parser.add_argument('id', required=True, type=int)
add_parser.add_argument('collaborators', required=True, type=str)
add_parser.add_argument('job', required=True, type=str)
add_parser.add_argument('work_size', required=True, type=int)
add_parser.add_argument('team_leader', required=True, type=int)
add_parser.add_argument('is_finished', required=True, type=bool)
add_parser.add_argument('categories', required=True, type=str)

edit_pasres = reqparse.RequestParser()
edit_pasres.add_argument('collaborators', required=True, type=str)
edit_pasres.add_argument('job', required=True, type=str)
edit_pasres.add_argument('work_size', required=True, type=int)
edit_pasres.add_argument('team_leader', required=True, type=int)
edit_pasres.add_argument('is_finished', required=True, type=bool)
edit_pasres.add_argument('categories', required=True, type=str)

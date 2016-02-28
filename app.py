import sqlite3
import json
from flask import Flask,g,jsonify
from flask_restful import Resource, Api, reqparse
from werkzeug.local import LocalProxy
app = Flask(__name__)
api = Api(app)

DATABASE = '/tmp/app.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		db.row_factory = sqlite3.Row
	return db

db = LocalProxy(get_db)

@app.teardown_appcontext
def close_connection(exception):
	if db is not None:
		db.close()

def query_db(query, args=()):
	cur = db.cursor()
	cur.execute(query, args)
	results = [dict(row) for row in cur]
	return results

def get_user_skills(email):
	return query_db('select name,rating from skill where userEmail = ?',[email])

def find_user_by_email(email):
	users = query_db('select * from user where email = ?', [email])
	for user in users:
		skills = get_user_skills(user['email'])
		user['skills'] = skills
		return user
	return None

def update_user(field, value, email):
	cur = db.cursor()
	query = 'update user set ' + field + ' = ? where email = ?'
	cur.execute(query, [value, email])
	db.commit()
	return None

def update_skill(name, userEmail, rating):
	cur = db.cursor()
	cur.execute('update skill set rating = ? where userEmail = ? and name = ?', [rating, userEmail, name])
	db.commit()
	return None

# parsers

basic_parser = reqparse.RequestParser()
user_basic_fields =['company','latitude','longitude','name','phone','picture']
for field in user_basic_fields:
	basic_parser.add_argument(field)

skills_parser = reqparse.RequestParser().add_argument('skills', type=list, location='json')

# resources

class User(Resource):
	def get(self, email):
		return find_user_by_email(email)
	def put(self, email):
		basic_args = basic_parser.parse_args()
		for field in user_basic_fields:
			if basic_args[field] is not None:
				update_user(field, basic_args[field], email)
		
		skills = skills_parser.parse_args()['skills']
		print skills
		if skills is not None:
			for skill in skills:
				update_skill(skill['name'], email, skill['rating'])

		return find_user_by_email(email)

class Users(Resource):
	def get(self):
		users = query_db('select * from user')
		for user in users:
			user['skills'] = get_user_skills(user['email'])
		return jsonify(results=users)

api.add_resource(User, '/users/<email>')
api.add_resource(Users, '/users')

if __name__ == "__main__":
	app.run(debug=True)

import sqlite3
import json
from flask import Flask,g,request,jsonify
from werkzeug.local import LocalProxy
app = Flask(__name__)

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
	# db = getattr(g, '_database', None)
	if db is not None:
		db.close()

# @app.cli.command('initdb')
def init_db():
	with app.app_context():
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
	print('Initialized the database.')

def query_db(query, args=()):
	cur = db.cursor()
	cur.execute(query, args)
	results = [dict(row) for row in cur]
	return results

def find_user_by_email(email):
	users = query_db('select * from user where email = ?', [email])
	for user in users:
		skills = query_db('select * from skill where userEmail = ?',[user['email']])
		user['skills'] = skills
		return user
	return None

@app.route("/users", methods=['POST', 'GET', 'PUT'])
def users():
	email = request.args.get('email')
	if email is not None:
		if request.method == 'GET':
			user = find_user_by_email(email)
			if user is not None :
				return jsonify(user)
			else :
				return 'User not found.'
		if request.method == 'PUT':
			phone = request.json.get('phone')
			
			print request.json.get('hello')
	else :
		if request.method == 'GET':
			users = query_db('select * from user')
			for user in users:
				user['skills'] = query_db('select * from skill where userEmail = ?',[user['email']])
				return jsonify(results=users)
	return "Hello World!"

if __name__ == "__main__":
	app.run(debug=True)

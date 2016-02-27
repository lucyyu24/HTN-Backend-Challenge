import sqlite3
import json

# initalize DB
DATABASE = '/tmp/app.db'
db = sqlite3.connect(DATABASE)
cursor = db.cursor()

# insert user
def insert_user(name, email, company, phone, latitude, longitude, picture):
	cursor.execute('''INSERT INTO user(name, email, company, phone, latitude, longitude, picture)
				VALUES(:name, :email, :company, :phone, :latitude, :longitude, :picture)''',
				{'name':name, 'email':email, 'company':company, 'phone':phone, 'latitude':latitude, 'longitude':longitude, 'picture':picture})
	db.commit()

# insert skill
def insert_skill(name, rating, userEmail):
	cursor.execute('''INSERT INTO skill(name, rating, userEmail)
				VALUES(:name, :rating, :userEmail)''', {'name':name, 'rating':rating, 'userEmail':userEmail})
	db.commit()

# load data from JSON file
with open('users.json') as data_file:    
		data = json.load(data_file)

# insert users and skills into DB
for user in data:
	insert_user(user['name'], user['email'], user['company'], user['phone'], user['latitude'], user['longitude'], user['picture'])
	for skill in user['skills']:
		insert_skill(skill['name'], skill['rating'], user['email'])
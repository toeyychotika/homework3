import pymongo

from flask  import Flask, request
from flask_restful import Resource, Api, reqparse

from datetime import datetime, date
from time import gmtime, strftime

import json

today = date.today()
temp=[]
checkPass=True

url = "mongodb://chotika:toeyy@localhost:27017/admin"
client = pymongo.MongoClient(url)

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('information')

db=client.admin.cpe_company_limited

class Registration(Resource):
	def post(self):
		args=parser.parse_args()
		data=json.loads(args['information'])
		db.update_one({"id":data['id']},
			{'$set':
			{"id":data['id'],
				"firstname":data['firstname'],
				"lastname":data['lastname'],
				"password":data['password'],
				"datetime":""
			}},upsert=True)
		return{'firstname':data['firstname']}

class Login(Resource):
	def post(self):
		args=parser.parse_args()
		data=json.loads(args['information'])
		result=db.find_one({'id':data['id']})
		if str(result['password']) != str(data['password']) :
			checkPass=False
			gg='invalid'
			return{'user':gg }
		else:
			checkPass=True
		if checkPass:
			datetime=str(strftime("%d-%m-%Y %H:%M:%S", gmtime()))
			temp.append(datetime)
			db.update_one({"id":data['id']},
				{'$set':
				{"id":data['id'],
					"datetime":temp
				}},upsert=True)
			return{'firstname':result['firstname'],'datetime':datetime}

class Check(Resource):
	def post(self):
		args=parser.parse_args()
		data=json.loads(args['information'])
		result=db.find_one({'id':data['id']})
		return{'datetime':result['datetime'],'name':result['firstname'],'id':result['id']}


api.add_resource(Login,'/api/login')
api.add_resource(Registration,'/api/reg')
api.add_resource(Check,'/api/check')

if __name__=='__main__':
	app.run(host='0.0.0.0',port=5001)





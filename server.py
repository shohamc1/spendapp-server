from flask import Flask
from flask_restful import Api, Resource, reqparse
import os
import json
import pymongo
#from run import app

app = Flask(__name__)
api = Api(app)

client = pymongo.MongoClient("mongodb+srv://shohamc1:shohamc19960@cluster0-xcamt.gcp.mongodb.net/test?retryWrites=true&w=majority")
mydb = client['appdatabase']
mycol = mydb['names']
allentries = mycol.find()

#users = []
#print (users[1])



class User (Resource):
    def get (self, uid):
        allentries = mycol.find()
        for testuser in allentries:
            if (uid == testuser["_id"]):
                return testuser, 200
        
        return "User not found", 404
    
    def post (self, uid):
        allentries = mycol.find()
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()

        for testuser in allentries:
            if (uid == testuser["_id"]):
                return "User with ID {} already exists".format(uid), 400
        
        user = {"_id": uid, "name": args["name"]}
        mycol.insert_one(user)
        return user, 201

    def put (self, uid):
        allentries = mycol.find()
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()

        for testuser in allentries:
            if (uid == testuser["_id"]):
                testuser["name"] = args["name"]
                mycol.update_one({"_id": uid},{"$set": {"name": args["name"]}})
                return testuser, 201
        
        user = {"_id": uid, "name": args["name"]}
        mycol.insert_one(user)
        return "UID {} has been added".format(uid), 201
    
    def delete (self, uid):
        allentries = mycol.find()
        mycol.delete_one({"_id": uid})
        return "{} has been deleted".format(uid), 200

api.add_resource(User, "/user/<int:uid>")

#for testing
#app.run(debug=True)

#for deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
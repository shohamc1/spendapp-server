from flask import Flask
from flask_restful import Api, Resource, reqparse
import os
import json
import pymongo
from deployinfo import username, password
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

#from run import app

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

client = pymongo.MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0-xcamt.gcp.mongodb.net/test?retryWrites=true&w=majority")
mydb = client['appdatabase']
mycol = mydb['names']
allentries = mycol.find()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()


class User (Resource):
    @auth.login_required
    def get (self, uid):
        allentries = mycol.find()
        for testuser in allentries:
            if (uid == testuser["_id"]):
                return testuser, 200
        
        return "User not found", 404
    
    @auth.login_required
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

    @auth.login_required
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
    
    @auth.login_required
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

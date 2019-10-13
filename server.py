from flask import Flask
from flask_restful import Api, Resource, reqparse
import os
#from run import app

app = Flask(__name__)
api = Api(app)

users = []

class User (Resource):
    def get (self, uid):
        for user in users:
            if (uid == user["uid"]):
                return user, 200
        return "User not found", 404
    
    def post (self, uid):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()

        for user in users:
            if (uid == user["uid"]):
                return "User with ID {} already exists".format(uid), 400
        
        user = {
            "uid": uid,
            "name": args["name"]
        }
        users.append(user), 201

    def put (self, uid):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()

        for user in users:
            if (uid == user["uid"]):
                user["name"] = args["name"]
                return user, 200
        
        user = {
            "uid": uid,
            "name": args["name"]
        }
        users.append(user)
        return user, 201
    
    def delete (self, uid):
        global users
        users = [user for user in users if user["uid"] != uid]
        return "{} has been deleted".format(uid), 200

api.add_resource(User, "/user/<int:uid>")
#app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
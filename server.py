from flask import Flask
from flask_restful import Api, Resource, reqparse
import os
import json
#from run import app

app = Flask(__name__)
api = Api(app)

with open('.\data.json') as f:
    data = json.load(f)
    users = data['data']
#users = []
#print (users[1])

class User (Resource):
    def get (self, uid):
        for testid in range(0, len(users)):
            if (uid == users[testid]["uid"]):
                return users[testid], 200
        return "User not found", 404
    
    def post (self, uid):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()

        for testid in range(0, len(users)):
            if (uid == users[testid]["uid"]):
                return "User with ID {} already exists".format(uid), 400
        
        user = {"uid": uid, "name": args["name"]}
        users.append(user)
        with open('.\data.json', 'w') as f:
            json.dump(data, f), 201

    def put (self, uid):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()

        for testid in range(0, len(users)):
            if (uid == users[testid]["uid"]):
                users[testid]["name"] = args["name"]
                with open('.\data.json', 'w') as f:
                    json.dump(data, f)
                return users[testid], 201
        
        user = {"uid": uid, "name": args["name"]}
        users.append(user)
        with open('.\data.json', 'w') as f:
            json.dump(data, f)
        return "UID {} has been added".format(uid), 201
    
    def delete (self, uid):
        global users
        newusers = []
        for testid in range(0, len(users)):
            if users[testid]['uid'] != uid:
                newusers.append(users[testid])
        #users = [users[testid] for testid in range(0, len(users)) if users[testid]["uid"] != uid]
        data['data'] = newusers
        with open('.\data.json', 'w') as f:
            json.dump(data, f)
        return "{} has been deleted".format(uid), 200

api.add_resource(User, "/user/<int:uid>")

#for testing
app.run(debug=True)

#for deployment
#if __name__ == '__main__':
#    port = int(os.environ.get('PORT', 5000))
#    app.run(host='0.0.0.0', port=port)
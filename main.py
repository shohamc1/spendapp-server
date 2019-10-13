import json


with open('.\data.json') as f:
    data = json.load(f)

#DELETE
users = data['data']
newusers = []
for testid in range (0, len(users)):
    if users[testid]['uid'] != 3:
        newusers.append(users[testid])

users = newusers
print (newusers)


#POST and PUT
#input_id = input()
#input_name = input()

#a_dict = {"id": input_id, "name": input_name}
#data['data'].append(a_dict)

#with open('C:\\react\\PythonBackend\\data.json', 'w') as f:
#    json.dump(data, f)

#testing stuff
#print (data['data'][1]['id'])
#for person in data['data']:
#    person_name = person['name']
#    person_id = person['id']

#for GET
#num = (len(data['data']))

#for id in range (0, num):
#    if (data['data'][id]["uid"] == 3):
#        print (data['data'][id]['name'])

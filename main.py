import json
import sqlite3

conn = sqlite3.connect ('database.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS data (id int, name text)')

with open('C:\\react\\PythonBackend\\data.json') as f:
    data = json.load(f)

#print (data['data'][1]['id'])
for person in data['data']:
    person_name = person['name']
    person_id = person['id']

    c.execute('INSERT INTO data VALUES (' + person_id + ',"' + person_name + '")')
    conn.commit()

conn.close()
import json
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
mydb = client['uni']

data = {}

with open('database.json') as f:
    data = json.load(f)
with open('../webscraper/scrapedData.json') as fi:
    scrapedData = json.load(fi)

#update to database.json
for x in range(0,len(scrapedData)):
    i = len(data)
    data.update({
        i:{
        "intent": scrapedData[x]['intent'],
        "userquery": scrapedData[x]['userquery'],
        "response": scrapedData[x]['response']
        }
    })
    print("Updated " + str(x+1) + " record(s) to database.json")

with open('database.json', 'w') as json_file:
    json.dump(data, json_file)


#update to MongoDB
with open('database.json') as json_fi:
    database = json.load(json_fi)
    for i in range (len(database)):
        i = str(i) 
        try:
            myrecord = {
                "intent": data[i]['intent'] ,
                "userquery": data[i]['userquery'] ,
                "response": data[i]['response'] 
             }
            record_id = mydb.uni.insert(myrecord)
            print("Updated " + str(int(i)+1) + " record(s) to MongoDB database")

        except KeyError:
            break




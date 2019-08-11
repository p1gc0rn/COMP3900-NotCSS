from flask import Flask,request,jsonify,render_template,session,make_response
from flask_pymongo import PyMongo,MongoClient
import os
import dialogflow
import requests
import json
import re
import uuid
import random

from language import *

set_lang = ""

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'uni'
app.config['MONGO_URI'] = 'mongodb://mongodb:27017/uni'
mongo = PyMongo(app)

@app.route('/')
def index():
    #set cookie for each user
    my_id = uuid.uuid4()
    resp = make_response(render_template('index.html'))
    resp.set_cookie('user', str(my_id))
    return resp

#send POST request to dialogflow to detect users' intent
@app.route('/send_message', methods=['POST','GET'])
def send_message():
    global set_lang
    my_id = request.cookies.get('user')
    message = request.form['message']
    URL = "https://api.dialogflow.com/v1/query?v=20150910"
    detected_lang = getLang(message, set_lang)
    set_lang = detected_lang
    PARAMS = {'query': message, 'lang': detected_lang,'sessionId':my_id,'timezone':'America/New_York'}

    HEADERS = {'Authorization': 'Bearer 457b41645fa14fdca0606a315b73543c', 'Content-Type':'application/json'}
    r = requests.get(url = URL, params = PARAMS, headers = HEADERS)
    
    
    data = r.json()
    #get the response from dialogflow
    fulfillment_text = data['result']['fulfillment']['speech']
    #if there is any URL link in the response
    link = re.findall(r'(https?://[^\s]+)',fulfillment_text)

    #Rich link preview
    prev_link={}
    if(link):
        for l in link:
            l = l.rstrip('.')
            prev_link = get_link_preview(l)
            if not(prev_link['image']):
                prev_link['image'] = 'https://yt3.ggpht.com/a/AGF-l7_fK0Hy4B4JO8ST-uGqSU69OTLHduk4Kri_fQ=s288-c-k-c0xffffffff-no-rj-mo'
            fulfillment_text = fulfillment_text.replace(l,"<a target=\"_blank\" href="+l+">"+l+"</a>")

    #check options in the response
    options = ""
    try:
        data['result']['fulfillment']['messages'][1]['payload']['options']
        options = data['result']['fulfillment']['messages'][1]['payload']['options']
    except IndexError:
        options = re.findall(r"\##(.*?)\##",fulfillment_text)
        if(options):
            fulfillment_text = fulfillment_text.split('?',1)[0] +"?"

    #update into database
    record = mongo.db.conversation
    record_id = record.insert({'user': message,'bot':fulfillment_text})

    response_text={ "message": fulfillment_text, "options":options, "rich_preview": prev_link}
    return jsonify(response_text)

#show all data in MongoDB
@app.route('/db', methods=['GET'])
def get_all_content():
  unibot = mongo.db.uni
  output = []
  for u in unibot.find():
    output.append({'intent': u['intent'],'userquery': u['userquery'],'response':u['response']})
  return jsonify({'result' : output})

#finding data regarding the intent
@app.route('/db/<intent>', methods=['GET'])
def get_one_record(intent):
  unibot = mongo.db.uni
  output = []
  for u in unibot.find():
    if u:
      output.append({'userquery': u['userquery'],'response':u['response']})
    else:
      output = "No such name"
  return jsonify({'result' : output})


@app.route('/records', methods=['GET'])
def get_record():
    unibot = mongo.db.conversation
    output = []
    for u in unibot.find():
        output.append({'user': u['user'],'bot': u['bot']})
    
    return jsonify({'result' : output})


@app.route('/db', methods=['POST'])
def add_record():
  unibot = mongo.db.uni
  intent = request.json['intent']
  userquery = request.json['userquery']
  response = request.json['response']

  record_id = unibot.insert({'intent': intent,'userquery':userquery,'response':response})
  new_record = unibot.find_one({'_id': record_id })
  output = {'intent': new_record['intent'],'userquery': new_record['userquery'],'response':new_record['response']}
  return jsonify({'result' : output})


def get_link_preview(link):
    PARAMS = {'key':'5d28734e3c03b884738b4332ababd678ca505f4e04f4d', 'q':link}
    URL = "http://api.linkpreview.net/"

    r = requests.get(url = URL, params = PARAMS)
    data = r.json()

    return data

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')

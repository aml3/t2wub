from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
import hashlib
import urllib
import re

app = Flask(__name__)

account_sid = "" # TODO: read from file
auth_token = "" # TODO: read key from file
client = TwilioRestClient(account_sid, auth_token)

@app.route("/", methods=['GET', 'POST'])

def hello_monkey():
	resp = twilio.twiml.Response()
	messages = client.messages.list()
	message = messages[0]
	url = hashlib.sha256(message.body).hexdigest()[:8]
	if re.match("^\+1[0-9]{10}", message.body[0:12]): 
		data = urllib.urlencode({"commentText": message.body[12:]})
	else:
		data = urllib.urlencode({"commentText": message.body})
	u = urllib.urlopen("http://cs4414.cloudapp.net/wubbify/"+url, data)
	wubURL = u.read()
	resp.message(wubURL)
	if re.match("^\+1[0-9]{10}", message.body[0:12]):
		call = client.calls.create(to=message.body[0:12], from_="+17035968978", url="http://cs4414.cloudapp.net/song/"+url)
		print call.sid
	return str(resp)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1414, debug=True)

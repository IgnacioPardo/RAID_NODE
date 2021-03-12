from flask import Flask, send_from_directory, request, Response
import requests
import codecs, json
import os

from packages import *
check_for_pkg("psutil")

#DB
from database import DB

defaults = {}
db = DB("db.p", defaults)

#Threading
from threading import Thread

#WSGIServer
from gevent.pywsgi import WSGIServer

#Disable Warnings
import warnings

#warnings.filterwarnings('ignore')

#Logging
import logging

"""
#Logging configuration set to debug on debug.log file
logging.basicConfig(filename='debug.log',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

#Disable unneeded dependencies logging
werkzeugLog = logging.getLogger('werkzeug')
werkzeugLog.disabled = True
requestsLog = logging.getLogger('urllib3.connectionpool')
requestsLog.disabled = True
"""
def run():
	#WSGIServer
	WSGIServer(('', 8081), app).serve_forever()

#Thread
def keep_alive():
	t = Thread(target=run)
	t.start()

app = Flask(__name__)

@app.route('/')
def main():
	return '<body style="background:black;font-family: Futura"><style type="text/css">a:link {color: white;} a:visited {color: white;} a:hover {color: white;} a:active {color: white;} </style><br><center><a class="RAID_NODE" href="'+node_loc+'">' + os.getenv("REPL_SLUG") + '</a></center></body>'

@app.route('/usage')
def usage():
	return {"ram": db.ram_usage_p(), "disk": db.disk_usage_p()}

@app.route('/getAll')
@app.route('/get')
@app.route('/get/<_id>')
def _get(_id=None):
	if _id:
		return str(db.get(_id))
	return str(db.getAll())

@app.route('/set', methods=['POST'])
@app.route('/set/<_id>', methods=['POST'])
def _set(_id=None):
	if request.method == 'POST':
		_id = db.set(json.loads(request.form["request"]), _id)
		try:
			_id = db.set(json.loads(request.form["request"]), _id)
			return {'success': True, 'id_set': _id}
		except:
			return {'success': False, "error": None}
	return {'success': False, "error": None}

def announce_self():
	x = requests.post('https://RAIDHUB.'+os.getenv("REPL_OWNER")+'.repl.co/announce_self', data = {'request': json.dumps({'node_url': node_loc})})

	resp = json.loads(x.text) 

	if resp["success"]:
		return resp["node_id"]
	return False

if __name__ == '__main__':
	#Run server forever
	node_loc = str("https://" + os.getenv("REPL_SLUG") + "." + os.getenv("REPL_OWNER") + ".repl.co").lower()
	
	if not os.getenv("node_id"):
		while not (node_id := announce_self()):
			continue
		print(node_id)
		os.environ['node_id'] = node_id
	
	keep_alive()

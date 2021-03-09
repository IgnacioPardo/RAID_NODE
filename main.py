from flask import Flask, send_from_directory, request, Response
import codecs, json
import os

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
warnings.filterwarnings('ignore')

#Logging
import logging

#Logging configuration set to debug on debug.log file
logging.basicConfig(filename='debug.log',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

#Disable unneeded dependencies logging
werkzeugLog = logging.getLogger('werkzeug')
werkzeugLog.disabled = True
requestsLog = logging.getLogger('urllib3.connectionpool')
requestsLog.disabled = True

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
	return '<a href="'+node_loc+'">' + node_loc + '</a>'

@app.route('/usage')
def usage():
	print(request.remote_addr)
	return {"ram": db.ram_usage_p(), "disk": db.disk_usage_p()}

@app.route('/getAll')
@app.route('/get')
@app.route('/get/<_id>')
def _get(_id=None):
	if _id:
		return db.get(_id)
	return db.getAll()

@app.route('/set', methods=['POST'])
@app.route('/set/<_id>', methods=['POST'])
def _set(_id=None):
	if request.method == 'POST':
		try:
			_id = db.set(json.loads(request.form["request"]), _id)
			return {'id_set': _id}
		except:
			return 400
	return 400

if __name__ == '__main__':
	#Run server forever
	node_loc = str("https://" + os.getenv("REPL_SLUG") + "." + os.getenv("REPL_OWNER") + ".repl.co").lower()

	keep_alive()
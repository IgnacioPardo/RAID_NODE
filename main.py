from flask import Flask, send_from_directory
import codecs
import os

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
	return 

if __name__ == '__main__':
	#Run server forever
	keep_alive()

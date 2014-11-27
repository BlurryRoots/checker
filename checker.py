import os
import psutil
import requests
import json
import sys
from threading import Timer
from optparse import OptionParser

class Checker ():
	CHECK_INTERVAL = 3
	def __init__ (self, options):
		self.options = options
		self.timer = None
		self.active = True
		self.report_url = 'http://%s:%s/report' % (options.monitor_host, options.monitor_port)
		self.host = options.host
		self.port = options.port
	def start (self):
		self.timer = Timer (Checker.CHECK_INTERVAL, self.on_timer)
		self.timer.start ()
	def on_timer (self):
		if self.check ():
			self.send_report ()
		if self.active:
			self.start ()
	def check (self):
		fp = self.options.pid_file_path
		if not os.path.isfile (fp):
			return False
		pid = -1
		with open (fp) as pid_file:
			pid = int (pid_file.read())
			print "Checking if pid %d exists." % pid
		if psutil.pid_exists (pid):
			return True
		else:
			return False
	def is_running (self):
		return self.active
	def shutdown (self):
		self.active = False
		self.timer.cancel ()
	def send_report (self):
		r = requests.post (self.report_url,
			data = json.dumps ({
				'host': self.host,
				'port': self.port
			}),
			headers = {
				'content-type': 'application/json'
			}
		)
		print 'Monitor responded (%d): %s' % (r.status_code, r.text)

parser = OptionParser()
parser.add_option('-f', '--pid-file', dest='pid_file_path',
	action='store', type='string',
	help="Path to rails pid file.")
parser.add_option("-r", "--monitor-host", dest="monitor_host",
	help="IP where monitor is accessible.")
parser.add_option("-R", "--monitor-port", dest="monitor_port",
	action='store', type='int',
	help="Port on which monitor is listening.")
parser.add_option("-n", "--host", dest="host",
	help="External ip.")
parser.add_option("-N", "--port", dest="port",
	action='store', type='int',
	help="External port.")

(options, args) = parser.parse_args ()

#
checker = Checker (options)
checker.start ()
running = True
while running:
	# check if pid is in process list
	try:
		if not checker.is_running ():
			running = False
	except (KeyboardInterrupt, SystemExit):
		checker.shutdown ()
		print '\nReceived KeyboardInterrupt.'

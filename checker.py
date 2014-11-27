import os
import psutil
import requests
import json
import sys
import time
from threading import Timer
from optparse import OptionParser

class Checker ():
	"""This class is responsible for checking the status of a process.
	   Checker reads a process id from a pid file and then double checks if
	   the read pid is currently present in the list of running processes."""
	CHECK_INTERVAL = 3
	def __init__ (self, options):
		self.options = options
		self.timer = None
		self.active = True
		self.report_url = 'http://%s:%s/report' % (options.monitor_host, options.monitor_port)
		self.host = options.host
		self.port = options.port
	def start (self):
		"""Starts the timer"""
		self.timer = Timer (Checker.CHECK_INTERVAL, self.on_timer)
		self.timer.start ()
	def on_timer (self):
		"""This method is called, when the timer has expired"""
		if self.check ():
			self.send_report ()
		if self.active:
			self.start ()
	def check (self):
		"""Here we check if the pid file is present, and if so
		   whether the pid is also present in the list of running processes"""
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
		"""Returns the current working status of checker"""
		return self.active
	def shutdown (self):
		"""Shuts down checker, including its timer"""
		self.active = False
		self.timer.cancel ()
	def send_report (self):
		"""This method reports the status of the node on which checker runs
		   to the predefinded adress on which the monitor server is running."""
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
parser.add_option('-f', '--pid-file',
	dest='pid_file_path',
	action='store', type='string',
	help="Path to rails pid file.")
parser.add_option("-r", "--monitor-host",
	dest="monitor_host",
	help="IP where monitor is accessible.")
parser.add_option("-R", "--monitor-port",
	dest="monitor_port",
	action='store', type='int',
	help="Port on which monitor is listening.")
parser.add_option("-n", "--host",
	dest="host",
	action='store', type='string',
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
	"""Run as long as there has not been a keyboard interrupt, triggered
	   by ctrl+c"""
	try:
		if not checker.is_running ():
			running = False
		else:
			time.sleep (1)
	except (KeyboardInterrupt, SystemExit):
		checker.shutdown ()
		print '\nReceived KeyboardInterrupt.'

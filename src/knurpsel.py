#
from flask import *
from threading import Timer
#
import json


# create utility classes
class ServerNode ():
	"""Represents a server node. Used to document the host,
	   port and state of the server node."""
	NODE_TIMEOUT = 5
	def __init__ (self, host, port):
		self.host = host
		self.port = port
		self.activate ()
		self.timer = None
	def get_host (self):
		return self.host
	def get_port (self):
		return self.port
	def activate (self):
		self.active = True
	def timeout (self):
		print '%s:%s timed out!' % (self.host, self.port)
		self.active = False
	def is_active (self):
		return self.active
	def to_json (self):
		return '{"host":"%s", "port":%d, "active":%s}' % (
			self.host,
			self.port,
			self.active and 'true' or 'false'
		)

class NodeDatabase ():
	"""Holds all nodes, which had been reporting, since the monitor
	   service has been started. A node 'times out' after a given number
	   of seconds, which means it is probably dead."""
	def __init__ (self):
		self.nodes = {}
		self.timeout_timers = {}
	def as_list (self):
		node_list = []
		for node_name, node in self.nodes.iteritems ():
			node_list.append ({
				'host': node.get_host (),
				'port': node.get_port (),
				'active': node.is_active ()
			})
		return node_list
	def update (self, node_info):
		host = node_info['host']
		port = node_info['port']
		key = '%s:%s' % (host, port)
		if not key in self.nodes:
			self.nodes[key] = ServerNode (host, port)
		node = self.nodes[key]
		node.activate ()
		if not key in self.timeout_timers:			
			self.timeout_timers[key] = Timer (ServerNode.NODE_TIMEOUT, self.on_timeout, [key])
		self.timeout_timers[key].start ()
	def on_timeout (self, key):
		self.nodes[key].timeout ()
		del self.timeout_timers[key]

class BaseView ():
	"""Base class for jinja templates. Should be used by controllers
	   if they want to render stuff."""
	def __init__ (self, path):
		self.view_path = path
	def render (self, *data, **data_map):
		return render_template (self.view_path, **data_map)

class ReportController ():
	"""Controller responsible for doing all task related to reporting."""
	def __init__ (self):
		self.nodes = NodeDatabase ()
		self.view = BaseView ('report.html')
	def index_get_json (self, request):
		return Response (json.dumps (self.nodes.as_list ()), status=200)
	def index_get (self, request):
		view_str = self.view.render (nodes=self.nodes.as_list ())
		return Response (view_str, status=200)
	def index_post (self, request):
		r = None
		ct = request.headers['Content-Type']

		if ct == 'application/json':
			json_obj = request.json
			self.nodes.update (json_obj)
			r = Response ("thanks for reporting your status!", status=200)
		else:
			r = Response ("unexpected Content-Type: " + ct)

		return r
	def default (self, request):
		return Response ('unexpected request!', status=404)

class IndexController ():
	"""Controller responsible for handling all index actions"""
	def __init__ (self):
		self.link_to_report = '/report'
		self.view = BaseView ('index.html')
	def index_get (self, request):
		return self.view.render (link=self.link_to_report)

# app configuration
app = Flask (__name__)
app.controllers = {}
app.controllers['report'] = ReportController ()
app.controllers['index'] = IndexController ()

@app.route ("/")
def respond_index ():
	c = app.controllers['index']
	r = c.index_get (request)
	return r

@app.route ('/report.json', methods=['GET'])
def respond_report_json ():
	c = app.controllers['report']
	r = c.index_get_json (request)
	return r

@app.route ("/report", methods=['GET', 'POST'])
def respond_report ():
	c = app.controllers['report']
	r = None
	if request.method == 'POST':
		r = c.index_post (request)
	elif request.method == 'GET':
		r = c.index_get (request)
	else:
		r = c.default (request)
	return r

if __name__ == "__main__":
	app.run (host='0.0.0.0', port=4242, debug=True)

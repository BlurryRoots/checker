from flask import *

import json

app = Flask (__name__)

class NodeList ():
	def __init__ (self):
		self.nodes = ()
	def set (self, nodes):
		self.nodes = nodes
	def get (self):
		return self.nodes

class BaseView ():
	def __init__ (self, path):
		self.view_path = path
	def render (self, *data, **data_map):
		return render_template (self.view_path, **data_map)

class ReportController ():
	def __init__ (self):
		self.nodes = NodeList ()
		self.view = BaseView ('report.html')
	def index_get (self, request):
		view_str = self.view.render (nodes=self.nodes.get ())

		return Response (view_str, status=200)
	def index_post (self, request):
		r = None
		ct = request.headers['Content-Type']

		if ct == 'application/json':
			self.nodes.set (request.json)
			r = Response ("jowjow", status=200)
		else:
			r = Response ("unexpected Content-Type: " + ct)

		return r
	def default (self, request):
		return Response ('unexpected request!', status=404)

class IndexController ():
	def __init__ (self):
		self.link_to_report = '/report'
		self.view = BaseView ('index.html')
	def index_get (self, request):
		return self.view.render (link=self.link_to_report)


app.controllers = {}
app.controllers['report'] = ReportController ()
app.controllers['index'] = IndexController ()

@app.route ("/")
def keks ():
	c = app.controllers['index']
	r = None

	r = c.index_get (request)

	return r

@app.route ("/report", methods=['GET', 'POST'])
def report ():
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
	print "am i running?"
	app.run (host='0.0.0.0', port=4242, debug=True)

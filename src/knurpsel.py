from flask import *
import json

app = Flask (__name__)

app.currentTemplate = "Jow jow"

class NodeList():
	def __init__(self):
		self.nodes = {}

def update (data):
	app.currentTemplate = render_template ('index.html', nodes=data)

@app.route ("/")
def keks ():
	return app.currentTemplate

@app.route ("/report", methods=['GET', 'POST'])
def report ():
	r = Response ("unexpected error!", status=404)

	if request.method == 'POST':
		ct = request.headers['Content-Type']
		if ct == 'application/json':
			data = json.dumps (request.json)
			print "data: " + data
			update (request.json)
			r = Response ("jowjow", status=200)
		else:
			r = Response ("unexpected Content-Type: " + ct)
	else:
		r = Response ("danke!", status=200)

	return r

if __name__ == "__main__":
	print "am i running?"
	app.run (host='0.0.0.0', port=4242, debug=True)

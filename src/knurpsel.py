from flask import *
import json

app = Flask (__name__)

@app.route ("/")
def keks ():
	return "Knurpsel purzel!"

@app.route ("/report", methods=['GET', 'POST'])
def report ():
	r = Response ("unexpected error!", status=404)

	if request.method == 'POST':
		ct = request.headers['Content-Type']
		if ct == 'application/json':
			print json.dumps (request.json)
			r = Response ("jowjow", status=200)
		else:
			r = Response ("unexpected Content-Type: " + ct)
	else:
		r = Response ("hey there!", status=200)

	return r

if __name__ == "__main__":
	print "am i running?"
	app.run (host='0.0.0.0', port=4242)

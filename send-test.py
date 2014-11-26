import requests
import json

port = 8080
url = 'http://localhost:%d/report' % port
payload = ({
	'name': 'karl-otto',
	'load': 23,
	'status': True
}, {
	'name': 'horst-hubert',
	'load': 42,
	'status': True
})
ctype = {
	'content-type': 'application/json'
}

r = requests.post (url, data=json.dumps(payload), headers=ctype)

print "response\n\ttext: %s\n\tstatus: %d" % (r.text, r.status_code)

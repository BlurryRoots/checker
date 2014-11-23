import requests
import json

port = 8080
url = 'http://localhost:%d/report' % port
payload = {
	'who': 'karl-otto'
}
ctype = {
	'content-type': 'application/json'
}

r = requests.post (url, data=json.dumps(payload), headers=ctype)

print "response\n\ttext: %s\n\tstatus: %d" % (r.text, r.status_code)

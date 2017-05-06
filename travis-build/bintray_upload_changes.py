#!/usr/bin/python

from debian import deb822
import io
import requests
import os
import sys
import json
import re

def versioncmp(version1, version2):
	def normalize(v):
		return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
	a = normalize(version1)
	b = normalize(version2)
	return (a > b) - (a < b)

if len(sys.argv) < 4:
	print("Usage: {app} user repository changes_file".format(app= sys.argv[0]))
	sys.exit(0)

user = sys.argv[1]
repository = sys.argv[2]
changesFile = sys.argv[3]
apikey = os.environ["BINTRAY_API_KEY"]
passphrase = os.environ["BINTRAY_PASSPHRASE"]

with io.open(changesFile, 'rb') as f:
	d = deb822.Changes(f)
	url = "https://api.bintray.com/content/{user}/{repo}/{package}/{version}/pool/{component}/{package[0]}/{package}/{file};deb_distribution={distributions};deb_component={component};deb_architecture={architectures};publish=1;override=1"
	baseDir = os.path.dirname(os.path.realpath(changesFile))
	
	for file in d['Files']:
		if os.path.splitext(file['name'])[1] != '.deb':
			continue

		parameters = {
                        'user': user,
                        'repo': repository,
                        'package': d['Source'],
                        'version': d['Version'],
                        'file': file['name'],
                        'distributions':'unstable',
                        'component':'main',
                        'architectures':'amd64,i386'
                }
		finalUrl = url.format(**parameters)
		finalFile = baseDir + '/' + file['name']

		print("Sending package {} using parameters:\n{}".format(finalFile, json.dumps(parameters, indent=4)))
		with io.open(finalFile, "rb") as packageFile:
			headers = {'X-GPG-PASSPHRASE': passphrase}
			if versioncmp(requests.__version__, '0.8.3') >= 0:
				auth=requests.auth.HTTPBasicAuth(user, apikey)
			else:
				auth=('basic', user, apikey)
			r = requests.put(finalUrl, headers=headers, auth=auth, data=packageFile)
			print("Response: {}".format(r.text))


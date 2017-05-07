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

if versioncmp(requests.__version__, '0.8.3') >= 0: 
	auth=requests.auth.HTTPBasicAuth(user, apikey)
else:   
	auth=('basic', user, apikey)


def send_file(parameters, auth, baseDir, file):
	url = "https://api.bintray.com/content/{user}/{repo}/{package}/{version}/pool/{component}/{package[0]}/{package}/{file};deb_distribution={distributions};deb_component={component};deb_architecture={architectures};publish=0;override=1"
	finalUrl = url.format(**parameters, file=file)
	finalFile = baseDir + '/' + file

	print("Sending package {} using parameters:\n{}".format(finalFile, json.dumps(parameters, indent=4)))
	with io.open(finalFile, "rb") as packageFile:
		headers = {'X-GPG-PASSPHRASE': passphrase}
		r = requests.put(finalUrl, headers=headers, auth=auth, data=packageFile)
		print("Response: {}".format(r.text))

def publish_files(parameters, auth):
	url = "https://api.bintray.com/content/{user}/{repo}/{package}/{version}/publish"
	finalUrl = url.format(**parameters)
	
	print("Publishing files")

	headers = {'X-GPG-PASSPHRASE': passphrase}
	r = requests.post(finalUrl, headers=headers, auth=auth, json={"publish_wait_for_secs": -1})
	print("Response: {}".format(r.text))
        

def check_files(parameters, auth, change_file):
	url = "https://api.bintray.com/packages/{user}/{repo}/{package}/versions/{version}/files"
	finalUrl = url.format(**parameters)

	print("Checking sha256 sums")

	r = requests.get(finalUrl, auth=auth)
	checksums = { file['name']: file['sha256'] for file in r.json() }
	print(checksums)
	for changed_file in change_file['Checksums-Sha256']:
		if os.path.splitext(changed_file['name'])[1] == '.buildinfo':
			continue

		if changed_file['sha256'] != checksums[changed_file['name']]:
			raise Exception("Bad checksum on file {file}, local is {local}, bintray has {remote}".format(file=changed_file['name'], local=changed_file['sha256'], remote=checksums[changed_file['name']]))
		else:
			print("{file}: OK".format(file=changed_file['name']))



with io.open(changesFile, 'rb') as f:
	d = deb822.Changes(f)
	baseDir = os.path.dirname(os.path.realpath(changesFile))
	parameters = {
		'user': user,
		'repo': repository,
		'package': d['Source'],
		'version': d['Version'],
		'distributions':'unstable',
		'component':'main',
		'architectures':'amd64,i386'
	}

	for file in d['Files']:
		file_type = os.path.splitext(file['name'])[1]
		if file_type == '.buildinfo':
			continue

		send_file(parameters, auth, baseDir, file['name'])

	publish_files(parameters, auth)
	check_files(parameters, auth, d)

from requests_html import HTMLSession
from requests import get
import urllib.request
import re, shutil, os, sys


pages = 22
results = []
links = []
base_url = 'https://standardebooks.org'


session = HTMLSession()
c = 0
for i in range(1, pages):
	url = base_url + '/ebooks/?page={}'.format(str(i))
	r = session.get(url)

	for x in r.html.links:
		if re.search('\/ebooks\/.*\/.+$', x):
			c += 1
			results.append(x)
	print('\rScraped {} pages, found {} books'.format(i, c), end='')

print('\nFound {} books. Building URLs...'.format(len(results)))

for x in results:
	info = x.split('/')
	del info[:2]

	url = "{}/dist/{}_{}.epub".format(x, info[0], info[1])
	info.append(url)
	links.append(info)

print('Done building URLs')

for book in links:
	title = book[1].replace('-', ' ').title()
	author = book[0].replace('-', ' ').title()

	print('\rGrabbing book {} by {}'.format(title, author, end=''))

	info = book[-1].split('/')
	with open('{}/{}'.format(os.getcwd(), info[-1]), 'wb+') as file:
		r = get(base_url + book[-1])
		file.write(r.content)

print('Done! Enjoy!')
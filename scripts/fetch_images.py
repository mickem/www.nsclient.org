#!/bin/python
from os import walk, makedirs, remove
from os.path import isfile, join, exists, abspath
from dateutil.parser import parse
from shutil import move
import re
import urllib
blog_folder = "content/blog"

def replace_images(lines):
	for l in lines:
		m = re.match(r'.*(\/wp.*(png|jpg))', l)
		if m:
			t = m.group(1).split('/')[-1].replace('\\', '_')
			print "%s => %s"%(m.group(1), t)
			
			urllib.urlretrieve ("http://www.nsclient.org%s"%m.group(1), 'content/images/blog/%s'%t)
		#else:
		#	print l
	return lines

files = []
for (dirpath, dirnames, filenames) in walk(blog_folder):
	for f in filenames:
		fpath = join(dirpath, f)
		if isfile(fpath) and f.endswith('.md'):
			files.append(fpath)
for fpath in files:
	lines = []
	#print " + %s"%fpath
	with open(fpath, 'r') as f:
		replace_images(f.readlines())

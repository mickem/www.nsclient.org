#!/bin/python
from os import walk, makedirs, remove
from os.path import isfile, join, exists, abspath
from dateutil.parser import parse
from shutil import move

blog_folder = "content/blog"

files = []
for (dirpath, dirnames, filenames) in walk(blog_folder):
	for f in filenames:
		fpath = join(dirpath, f)
		if isfile(fpath) and f.endswith('.md'):
			files.append(fpath)
for fpath in files:
	lines = []
	with open(fpath, 'r') as f:
		date = ''
		slug = ''
		cat = ''
		for l in f.readlines():
			if l.startswith("Date: "):
				date =parse(l[6:].strip()).strftime('%Y-%m-%d')
			elif l.startswith("Slug: "):
				slug = l[6:].strip()
			elif l.startswith("Category: "):
				cat = l[10:].strip().lower()
			else:
				lines.append(l)
	if not slug or not cat or not date:
		print "Missing metadata in %s (%s, %s, %s)"%(fpath, slug, cat, date)
		continue
	target_path = '%s/%s/%s/%s'%(blog_folder, cat, date, slug)
	target_name = 'post.md'
	target = join(target_path, target_name)
	if not exists(target_path):
		makedirs(target_path)
	s = abspath(fpath)
	d = abspath(target)
	if s != d:
		print fpath, " -> ", target
		remove(fpath)
		with open(target, 'w') as f:
			print 'Saving: %s'%target
			f.writelines(lines)
	else:
		print "skipping: %s"%fpath

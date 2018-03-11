#!/usr/bin/env python3
import os, sys
import stat
from pathlib import Path
from datetime import *
import time
import re


def lspython(file,fileName):
	permission = stat.filemode(os.stat(file).st_mode)
	link = os.stat(file).st_nlink
	p_owner = Path(file).owner()
	p_group = Path(file).group()
	size = os.stat(file).st_size
	# referred to https://stackoverflow.com/questions/10256093/how-to-convert-ctime-to-datetime-in-python
	time = datetime.fromtimestamp(float(os.stat(file).st_ctime)).strftime("%b %d %H:%M")
	print(permission+' '+str(link)+' '+p_owner+' '+p_group+' '+str(size)+' '+str(time)+' '+fileName)

# handle corner case: no file path in command line
if len(sys.argv) <= 1: 
	p = Path.cwd()
	lspython(str(p),'.')
	lspython(str(p.parent), '..')
	files = os.listdir(str(p))
	# discussed with Ziqing Zhang about the usage of regular expression
	sorted_files = sorted(files, key=lambda s: re.sub('[^0-9a-zA-Z]+', '', s).lower())
	for file in sorted_files:
		file_name = file
		file = p.joinpath(file)
		lspython(str(file),file_name)
else: 
	path = sys.argv[1:]
	for p in path:
		p = Path(p)
		if p.exists():
			if os.path.isfile(str(p)):
				lspython(str(p), str(p))
			elif os.path.isdir(str(p)):
				# p = p.glob('*')
				# show the information of '.' and '..' directory first
				lspython(str(p),'.')
				lspython(str(p.parent), '..')

				files = os.listdir(str(p))
				sorted_files = sorted(files, key = lambda s: re.sub('[^0-9a-zA-Z]+', '', s).lower())
				for file in sorted_files:
					file_name = file
					file = p.joinpath(file)
					lspython(str(file),file_name)
				
		else:
			print("ls: cannot access %s: No such file or directory\n" %sys.argv[1])

# referred to http://stackabuse.com/python-list-files-in-a-directory/
# referred to https://docs.python.org/3/library/stat.html


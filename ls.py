#!/usr/bin/env python3
import os, sys
import stat
from pathlib import Path
from datetime import *
import time
import re


# def get_mode(mode):
# 	perm = ''
# 	link = ''
# 	#deal with whether it is a file or a directory
# 	if stat.S_ISDIR(mode):
# 		perm = 'd'
# 	elif stat.S_ISLNK(mode):
# 		perm = 'l'
# 		link = os.readlink(mode)
# 	elif stat.S_ISREG(mode):
# 		perm = '-'
# 	else:
# 		sys.stderr.write("Cannot access %s: No such file or directory\n" %mode)
# 		return
# 	#deal with permissions
# 	m = stat.S_IMODE(mode)
# 	n = 100
# 	while (n > 0):
# 		temp = m
# 		if m // n == '7':
# 			perm = perm + 'rwx'
#         elif m // n == '6':
#         	perm = perm + 'rw-'
#         elif m // n == '5':
#             perm = perm + 'r-x'
#         elif m // n == '4':
#             perm = perm + 'r--'
#         elif m // n == '3':
#             perm = perm + '-wx'
#         elif m // n == '2':
#             perm = perm + '-w-'
#         elif m // n == '1':
#             perm = perm + '--x'
#         elif m // n == '0':
#         	perm = perm + '---'
#         temp = temp % n
#         n = n / 10
#     return perm

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


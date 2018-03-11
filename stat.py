#!/usr/bin/env python3

import os, stat
import sys
import datetime
from pwd import getpwuid
from pathlib import *
import pytz

# referred to https://docs.python.org/3.6/library/stat.html
def fileType(file):
	if stat.S_ISDIR(file) != 0:
		return 'directory'
	elif stat.S_ISCHR(file) != 0:
		return 'special file'
	elif stat.S_ISBLK(file) != 0:
		return 'block special file'
	elif stat.S_ISREG(file) != 0:
		return 'regular file'
	elif stat.S_ISFIFO(file) != 0:
		return 'pipe'
	elif stat.S_ISLNK(file) != 0:
		return 'symbolic link'
	elif stat.S_ISSOCK(file) != 0:
		return 'socket'
	elif stat.S_ISDOOR(file) != 0:
		return 'door'
	elif stat.S_ISPORT(file) != 0:
		return 'event port'
	elif stat.S_ISWHT(file) != 0:
		return 'whiteout'

# corner case: no operand
if len(sys.argv) < 2:
	print('stat: missing operand')
	print("Try 'stat --help' for more information.")

else:
	p = Path(sys.argv[1])
	if p.exists():
		fileStat = p.stat()
		File = sys.argv[1]
		Size = str(fileStat.st_size)
		Blocks = str(fileStat.st_blocks)
		IO_Block = str(fileStat.st_blksize)
		file_type = str(fileType(fileStat.st_mode))
		# referred to https://docs.python.org/3/library/functions.html#hex
		Device = str(hex(fileStat.st_dev)[-2:])+'h/'+str(fileStat.st_dev)+'d'
		Inode = str(os.stat(File).st_ino)
		Links = str(fileStat.st_nlink)
		Access1 = str(oct(fileStat.st_mode)[-4:])+"/"+str(stat.filemode(os.stat(File).st_mode))
		u_id = str(os.stat(sys.argv[1]).st_uid)+"/   "+str(p.owner())
		g_id = str(os.stat(sys.argv[1]).st_gid)+"/   "+str(p.group())

		print("File: '"+File+"'")
		print("Size: "+Size+"  Blocks:"+Blocks+"  IO Block:"+IO_Block+"  "+file_type)
		print("Device: "+Device+" Inode:"+Inode+" Links: "+Links)
		print("Access: ("+Access1+")"+"  Uid:("+u_id+")"+"   Gid:("+g_id+")")

		print("Access: "+str(pytz.timezone('America/Chicago').localize(datetime.datetime.fromtimestamp(fileStat.st_atime)).strftime('%Y-%m-%d %H:%M:%S.%f' +' %z')))
		print("Modify: "+str(pytz.timezone('America/Chicago').localize(datetime.datetime.fromtimestamp(fileStat.st_mtime)).strftime('%Y-%m-%d %H:%M:%S.%f'+' %z')))
		print("Change: "+str(pytz.timezone('America/Chicago').localize(datetime.datetime.fromtimestamp(fileStat.st_ctime)).strftime('%Y-%m-%d %H:%M:%S.%f'+' %z')))
		print(' Birth: -')
	else:
		print("stat: cannot stat '"+sys.argv[1]+"': No such file or directory")

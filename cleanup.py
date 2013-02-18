#!/usr/bin/python

# User defined variables go here:

path = "/home/jwr/totallysweet/video/unsorted"
videoextensions = ["mkv", "avi", "mp4"]
logfile = "/var/log/videocleanup.log"

# That's all

# -jwr, 20130205

import os
import os.path
import datetime
import logging

# Declare some functions first

# Get the file size of all the files in a list
def totaldirsize(path):
	dirsize = 0
	for file in os.listdir(path):
		dirsize += os.stat(path + "/" + file)[6]
	return dirsize

# Get the file size of an individual file
def filesize(fullpath):
        filesize = os.stat(fullpath)[6]
	return filesize

# Set up logging
#
# If you want errors and successful deletes to be logged,
# use level=logging.INFO. If you want only errors to be
# logged, use level=logging.ERROR

logging.basicConfig(filename=logfile,level=logging.INFO)


# Make a list of everything in the user specified path
toplist = os.listdir(path)

# Remove non-directories from toplist
for item in toplist:
	if os.path.isdir(path + "/" + item) == False:
		toplist.remove(item)

# Find which dirs have a show, put them in showlist
showlist = []
for dir in toplist:
	for file in os.listdir(path + "/" + dir + "/"):
		if file.lower()[-3:] in videoextensions:
			showlist.append(path + "/" + dir)
			break

# Get the size of each dir, and determine if videos are 90% of that size
ninetydirs = []
for dir in showlist:
	dirsize = totaldirsize(dir)
	files = os.listdir(dir + "/")
	for file in files:
		if file.lower()[-3:] not in videoextensions:
			files.remove(file)
	sizeofvideos = 0
	for file in files:
		sizeofvideos += filesize(dir + "/" + file)
	if sizeofvideos > dirsize * .9:
		ninetydirs.append(dir + "/")


# Remove all the files which aren't videos from the directories which
# have videos and the videos make up 90% of their size

for dir in ninetydirs:
	dirsize = totaldirsize(dir)
	# Set onebigfile to True if there is one single file which is
	# 90% of the size
	files = os.listdir(dir + "/")
	for file in files:
		if filesize(dir + "/" + file) > dirsize * .9 and \
		os.path.isfile(dir + "/" + file) and \
		file.lower()[-3:] in videoextensions:
			files.remove(file)
			onebigfile = True
			break
		else:
			onebigfile = False

	# If onebigfile is True, delete everything except the big file, 
	# even if we delete some videos
	if onebigfile == True:
		for file in files:
			try:
				os.remove(dir + "/" + file)
			except OSError as e:
				logging.error(e.strerror + ": could not delete " + dir + "/" + file)
			else:
				logging.info('Deleted ' + dir + "/" + file)
	# if onebigfile is False, delete everything that is not a video
	if onebigfile == False:
		for file in files:
			if file.lower()[-3:] not in videoextensions:
	                        try:
					os.remove(dir + "/" + file)
				except OSError as e:
					logging.error(e.strerror + ": could not delete " + dir + "/" + file)
				else:
					logging.info('Deleted ' + dir + "/" + file)

#	for file in os.listdir(dir):
#		if filesize(dir + "/" + file) < dirsize * .1 and \
#		os.path.isfile(dir + "/" + file):
#			try:
#				os.remove(dir + "/" + file)
#			except OSError as e:
#				logging.error(e.strerror + ": could not delete " + dir + "/" + file)
#			else:
#				logging.info('Deleted ' + dir + "/" + file)

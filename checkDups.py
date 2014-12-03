#!/usr/bin/python

from collections import defaultdict
import argparse
import os, sys
import hashlib

def interpretDict(dict):
	finalList = []
	for key in dict:
		if len(dict[key]) > 1:
			finalList.append(dict[key])
	return finalList

def hashFile(fileName):
	BLOCKSIZE = 65535
	try:
		hasher = hashlib.sha512()
		with open(fileName) as f:
			buffer = f.read(BLOCKSIZE)
			while len(buffer) > 0:
				hasher.update(buffer)
				buffer = f.read(BLOCKSIZE)
			f.close()
	except IOError as e:
		print "I/O error({0}). File {1}: {2}".format(e.errno, fileName, e.strerror)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise
	return hasher.hexdigest()

def checkDir(dir, depth):
	fileDict = defaultdict(list)
	for path, directories, files in os.walk(dir):
		for f in files:
			fileName = os.path.join(path, f)
			fileDict[hashFile(fileName)].append(fileName)
	return fileDict

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Check for duplicate files in a directory and sub directories')
	parser.add_argument('directory', metavar='Directory', type=str, help='A directory to search for duplicates in')
	# todo: add depth argument (through bfs)
	#parser.add_argument('-d', metavar='Depth', type=int, nargs='?', default='0')
	args = parser.parse_args()
	
	depth = 0 # will be args.d
	dir = args.directory

	fDict = checkDir(dir, depth)	

	for fileList in interpretDict(fDict):
		print fileList
		print '\n'

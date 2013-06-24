import os
import sys
import subprocess

PICTURE_FORMATS = ['JPG']

def path_to_convert():
	"""
	Returns the full path to the convert commant. Neet to find a
	better way of doing this.
	"""
	if sys.platform == 'darwin':
		return '/opt/ImageMagick/bin/convert'

def resize(src, dest, spec):
	"""
	Wrapper for resising a picture
	"""
	cmd = [path_to_convert(), '"%s"'%src, '-resize %s'%spec, '"%s"'%dest]
	print ' '.join(cmd)
	retcode = subprocess.call(' '.join(cmd), shell=True)
	print retcode

def get_files_in_folder(folder):
	"""
	Get a list of filenames in a folder
	"""
	files=[]
	for file in os.listdir(folder):
		fullpath = os.path.join(folder, file)
		ext = file[-3:].upper()
		if os.path.isfile(fullpath):
			if ext in PICTURE_FORMATS:
				files.append(file)
	return files

def process_folder(folder, outdir, operation, spec):

	# Checking if destination folder exists
	if os.path.exists(outdir)==False:
		print 'Creating folder %s' % outdir
		os.makedirs(outdir)

	# Processing the files
	for file in get_files_in_folder(folder):
		src = os.path.join(folder, file)
		dest = os.path.join(outdir, file)
		print 'Processing %s -> %s' % (src, dest)
		operation(src, dest, spec)


if __name__=='__main__':
	
	print path_to_convert()

	process_folder('/Users/danish/Pictures/Picasa Exports/500px',
		'/Users/danish/Pictures/Picasa Exports/500px/lowres/',
		resize, '10000@')
	
	#print get_files_in_folder(r'C:\Users\Danish\Pictures')

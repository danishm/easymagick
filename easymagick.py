import os
import sys
import argparse
import subprocess

PICTURE_FORMATS = ['JPG']

def path_to_convert():
	"""
	Returns the full path to the convert commant. Neet to find a
	better way of doing this.
	"""
	if sys.platform == 'darwin':
		# For Mac, programs on path are not available, hence have to give explicit paths
		return '/opt/ImageMagick/bin/convert'
	elif sys.platform == 'win32':
		# For windows, executable on the path seems to work just like thats
		return 'convert'


def resize(src, dest, spec):
	"""
	Wrapper for resising a picture
	"""
	cmd = [path_to_convert(), '"%s"'%src, '-resize %s'%spec, '"%s"'%dest]
	print ' '.join(cmd)
	retcode = subprocess.call(' '.join(cmd), shell=True)
	print retcode


def get_files_in_folder(folder, skip_existing=True):
	"""
	Get a list of filenames in a folder
	"""
	files=[]
	for file in os.listdir(folder):
		fullpath = os.path.join(folder, file)
		ext = file[-3:].upper()
		if os.path.isfile(fullpath):
			if ext in PICTURE_FORMATS:
				if os.path.exists(fullpath)==False or skip_existing==False:
					files.append(file)
				else:
					print 'Skipping: ', fullpath
	return files


def apply_batch_operation(folder_in, folder_out, operation, spec, skip_existing=True):
	"""
	Applies an operation as a batch to all files in a folder
	and stores the result in another folder
	"""
	# Checking if destination folder exists
	if os.path.exists(folder_out)==False:
		print 'Creating folder %s' % folder_out
		os.makedirs(folder_out)

	# Processing the files
	for file in get_files_in_folder(folder_in, skip_existing):
		src = os.path.join(folder_in, file)
		dest = os.path.join(folder_out, file)
		print 'Processing %s -> %s' % (src, dest)
		operation(src, dest, spec)


def process_folder(folder_in, subdir, operation, spec):
	"""
	Applies an operation as a batch to all files in a folder 
	and stores the result in a subdirectory in that folder
	"""
	folder_out = os.path.join(folder_in, subdir)
	apply_batch_operation(folder_in, folder_out, operation, spec)


RECIPES = {
	'screen': {
		'operation': resize, 'spec': '5000000@', 'subdir': '.screen'
	}
}


if __name__=='__main__':
	
	parser = argparse.ArgumentParser(description='Batch processor for photographs.')
	parser.add_argument('recipe', help='Batch processing recepies to use')
	parser.add_argument('folder', help='Full path to folder to apply to')
	
	args = parser.parse_args()

	if args.recipe in RECIPES:
		recipe_spec = RECIPES[args.recipe]
		process_folder(args.folder, recipe_spec['subdir'], recipe_spec['operation'], recipe_spec['spec'])
	else:
		print 'ERROR: Unknown recipe "%s"' % args.recipe
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
	#print ' '.join(cmd)
	retcode = subprocess.call(' '.join(cmd), shell=True)
	#print retcode


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
	for file in get_files_in_folder(folder_in):
		src = os.path.join(folder_in, file)
		dest = os.path.join(folder_out, file)

		if os.path.exists(dest)==False or skip_existing==False:
			print 'Processing %s -> %s' % (src, dest)
			operation(src, dest, spec)
		else:
			print 'Skipping: ', src
		


def process_folder(folder_in, subdir, operation, spec, skip_existing=True):
	"""
	Applies an operation as a batch to all files in a folder 
	and stores the result in a subdirectory in that folder
	"""
	folder_out = os.path.join(folder_in, subdir)
	apply_batch_operation(folder_in, folder_out, operation, spec, skip_existing)


RECIPES = {
	'screen': {
		'operation': resize, 'spec': '5000000@', 'subdir': '.screen'
	}
}


if __name__=='__main__':
	
	parser = argparse.ArgumentParser(description='Batch processor for photographs.')
	parser.add_argument('recipe', help='Batch processing recepies to use')
	parser.add_argument('folder', help='Full path to folder to apply to')
	parser.add_argument('-o', '--overwrite', action='store_true', default=False, help='Overwrite existing files')
	
	args = parser.parse_args()

	if args.recipe in RECIPES:
		recipe_spec = RECIPES[args.recipe]
		process_folder(args.folder, recipe_spec['subdir'], recipe_spec['operation'], recipe_spec['spec'], not args.overwrite)
	else:
		print 'ERROR: Unknown recipe "%s"' % args.recipe
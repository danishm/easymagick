easymagick.py
=============

A simpler python script to help with batch operations on images using the ImageMagick library. The library has a built in command `mogrify`, but its use is discouraged. This command was designed to edit image in-place and hence runs the risk of accidental loss of your source images if the command is not executed with the right flags.

They recommend using an `sh` shell loop to call the `convert` command. However, I wanted to make it OS independent since I use Windows, Mac OS X and Linux. I also wanted to have no additional dependencies other than the ImageMagick binaries and the standard Python library.

Usage
-----

The command requires a recipe name and the folder to apply the recipe to

	usage: easymagick.py [-h] recipe folder

	Batch processor for photographs.

	positional arguments:
	  recipe      Batch processing recepies to use
	  folder      Full path to folder to apply to

	optional arguments:
	  -h, --help  show this help message and exit

Example
-------

To resize images in a folder e.g. `M:\Pictures\Vacation\` for on-screen viewing and place them in a sub folder called "screen" e.g. `M:\Pictures\Vacation\screen\`, execute the following command.

	python easymagick.py screen M:\Pictures\Vacation\

Recipes
-------

Recipes are simple named templates to define the most typical batch processing actions that you need to do. The recipes are stores in the `RECIPES` variable in the `easymagick.py` script.

### Recipe: screen
My initial motivation for writing this script was to be able to reduce the size of my Digital SLR images from 24 Mega pixels to 5 Mega pixels i.e. adequate enough to view on a high resolution retina display without loss of quality. I wanted to store these re-sized images in sub-folder of each of my main picture folders.

Future Enhancements
-------------------

 * Ability to apply a batch operation to a whole folder hierarchy recursively.
 * Add more recipes.
 * Add ability to specify a batch operation manually from command line.

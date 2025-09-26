import os
import sys
import argparse
from .settings import CONF_DIR, __version__, DEFAULT_WALLPAPERS_DIR
from .db_helper import DbHelper
from .utils import rofi, set_wallpaper, setup

import glob

def get_args():
	'''Get the arguments'''

	parser = argparse.ArgumentParser(description='Wallpaper-maid helps with your wallpapers')
	parser.add_argument('-s', '--setup', action='store_true', help='Setup Wallpaper-maid')
	parser.add_argument('-v', '--version', action='store_true', help='Wallpaper-maid version')

	return parser.parse_args()

def parse_args(args, db):
	'''Parse the arguments'''

	if args.version:
		print(f'Wallpaper-maid v{__version__}')
		sys.exit(0)

	if args.setup:
		setup(db)
		sys.exit(0)

def wallpaper_maid():
	wall = []
	for file in glob.glob(f'{DEFAULT_WALLPAPERS_DIR}/*'):
		wall.append(f'{file}\0icon\x1f{file}')

	wallpaper = rofi(wall)
	if wallpaper:
		set_wallpaper(wallpaper)
		pass

def main():
	os.makedirs(CONF_DIR, exist_ok=True)
	db = DbHelper()

	args = get_args()
	parse_args(args, db)

	wallpaper_maid()
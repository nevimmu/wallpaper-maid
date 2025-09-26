import os
import sys
import argparse
from pathlib import Path
from .settings import CONF_DIR, __version__, DEFAULT_WALLPAPERS_DIR
from .db_helper import DbHelper
from .utils import rofi, set_wallpaper, setup

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

def wallpaper_maid(db):
	screens = db.get('screens')
	wallpapers_path = Path(DEFAULT_WALLPAPERS_DIR).rglob('*')

	suffix = []
	for _, _suffix in screens.items():
		suffix.append(f'-{_suffix}')
	
	wallpapers_list = []
	for file in wallpapers_path:
		_main = False
		_name = file.name.split('.')[0]

		if '-main' in _name:
			_main = True

		wallpapers_list.append({
			'name': _name, 
			'display_name': _name if not _main else _name.replace('-main', ''),
			'main': _main,
			'path': file
		})

	wallpaper_options = []
	for file in wallpapers_list:
		if any(suf in file['name'] and suf != '-main' for suf in suffix):
				continue
		
		wallpaper_options.append(f'{file['display_name']}\0icon\x1f{file['path']}')

	wallpaper_choice = rofi(wallpaper_options)
	if not wallpaper_choice:
		exit(0)

	chosen_wallpaper = next((wp for wp in wallpapers_list if wp['display_name'] == wallpaper_choice), None)
	if chosen_wallpaper['main']:
		'''If the chosen wallpaper is a main wallpaper, set wallpapers for all screens'''
		for screen, suffix in screens.items():
			suffixed_name = f'{chosen_wallpaper['display_name']}-{suffix}'
			suffixed_wallpaper = next((wp for wp in wallpapers_list if wp['name'] == suffixed_name), None)
			if suffixed_wallpaper:
				print(f'Setting wallpaper for {screen}: {suffixed_wallpaper['path']}')
				set_wallpaper(suffixed_wallpaper['path'], screen)
	else:
		set_wallpaper(chosen_wallpaper['path'])

def main():
	os.makedirs(CONF_DIR, exist_ok=True)
	db = DbHelper()

	args = get_args()
	parse_args(args, db)

	wallpaper_maid(db)
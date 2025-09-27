import os
import subprocess
import json
import questionary
from .settings import DEFAULT_THEME_PATH, THEME_PATH

def rofi(options):
	'''Display rofi menu with options and return the user choice'''
	options_str = '\n'.join(options)


	result = subprocess.run(
		['rofi', '-dmenu', '-p', 'Select a wallpaper', '-i', '-show-icons', '-config', THEME_PATH],
		input=options_str,
		text=True,
		capture_output=True
	)

	if result.returncode == 0:
		return result.stdout.strip()
	else:
		return None

def set_wallpaper(wallpaper_path, monitor=None):
	'''Set the wallpaper using swww'''
	if monitor:
		subprocess.run(['swww', 'img', wallpaper_path, '-o', monitor])
	else:
		subprocess.run(['swww', 'img', wallpaper_path])

def setup(db):
	'''Set the monitors names'''
	hypr_monitors = subprocess.run(
		['hyprctl', 'monitors', '-j'],
		capture_output=True,
	)

	monitors_json = json.loads(hypr_monitors.stdout)

	monitors = {}
	for m in monitors_json:
		print(m['name'])
		suffix = questionary.text(f'Choose monitor suffix for {m["name"]}').ask()
		monitors[m['name']] = suffix
	
	db.set('screens', monitors)
	print('Monitors set!')
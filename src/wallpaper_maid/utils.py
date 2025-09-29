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

def set_wallpaper(wallpaper_path, fps, monitor=None):
	'''Set the wallpaper using swww'''
	command = [
		'swww', 'img', wallpaper_path,
		'--transition-type', 'grow',
		'--transition-fps', str(fps)
		]

	if monitor:
		subprocess.run(command + ['-o', monitor])
	else:
		subprocess.run(command)

def setup(db):
	'''Set the monitors names'''
	hypr_monitors = subprocess.run(
		['hyprctl', 'monitors', '-j'],
		capture_output=True,
	)

	monitors_json = json.loads(hypr_monitors.stdout)

	monitors = {}
	for m in monitors_json:
		suffix = questionary.text(f'Choose monitor suffix for {m['name']}').ask()
		monitors[m['name']] = {
			'suffix': suffix,
			'fps': int(m['refreshRate'])
		}
	
	db.set('screens', monitors)
	print('Monitors set!')
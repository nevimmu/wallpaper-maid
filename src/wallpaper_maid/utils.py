import subprocess

def rofi(options):
	'''Display rofi menu with options and return the user choice'''
	options_str = '\n'.join(options)

	result = subprocess.run(
		['rofi', '-dmenu', '-p', 'Select a wallpaper', '-i', '-show-icons'],
		input=options_str,
		text=True,
		capture_output=True
	)

	if result.returncode == 0:
		return result.stdout.strip()
	else:
		return None

def set_wallpaper(wallpaper_path):
	'''Set the wallpaper using swww'''
	subprocess.run(['swww', 'img', wallpaper_path])
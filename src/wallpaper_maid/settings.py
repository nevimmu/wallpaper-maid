import os

__version__ = '0.3.0'

HOME = os.getenv('HOME', os.getenv('USERPROFILE'))
XDG_CONF_DIR = os.getenv('XDG_CONFIG_HOME', os.path.join(HOME, '.config'))

CONF_DIR = os.path.join(XDG_CONF_DIR, 'wallpaper-maid')
DEFAULT_WALLPAPERS_DIR = os.path.join(HOME, 'Pictures', 'Wallpapers')
MODULE_DIR = os.path.dirname(__file__)

DEFAULT_THEME_PATH = os.path.join(MODULE_DIR, 'theme.rasi')
CUSTOM_THEME_PATH = os.path.join(CONF_DIR, 'theme.rasi')

THEME_PATH = ''
if os.path.isfile(CUSTOM_THEME_PATH):
	THEME_PATH = CUSTOM_THEME_PATH
else:
	THEME_PATH = DEFAULT_THEME_PATH
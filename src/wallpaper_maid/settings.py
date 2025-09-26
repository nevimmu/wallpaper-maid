import os

__version__ = '0.0.1'

HOME = os.getenv('HOME', os.getenv('USERPROFILE'))
XDG_CONF_DIR = os.getenv('XDG_CONFIG_HOME', os.path.join(HOME, '.config'))

CONF_DIR = os.path.join(XDG_CONF_DIR, 'wallpaper-maid')
DEFAULT_WALLPAPERS_DIR = os.path.join(HOME, 'Pictures', 'Wallpapers')
MODULE_DIR = os.path.dirname(__file__)
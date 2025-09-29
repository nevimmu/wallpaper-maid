# Wallpaper Maid

A script to set your wallpaper using **rofi** and **swww** on **Hyprland**, with support for different wallpapers on each monitor.

## Installation

```bash
git clone https://github.com/nevimmu/wallpaper-maid
cd wallpaper-maid
pipx install .

wallpaper-maid -s # To setup the tool
```

## How to use
Wallpaper Maid will look for wallpapers in `~/Pictures/Wallpapers`. Run the following command to choose your wallpaper:  
`wallpaper-maid`

> [!IMPORTANT]
> When using the option to set a different wallpaper on each monitor, make sure to name your wallpapers according to the monitor suffix. For example:
> `wallpaper-main.png`, `wallpaper-right.png`, `wallpaper-left.png`

### Rofi theme
To use a custom theme, create or edit a theme file at:
`~/.config/wallpaper-maid/theme.rasi`
Rofi will automatically use this file when you run the script.
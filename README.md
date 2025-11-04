# Wallpaper Maid

A script to set your wallpaper using **rofi** and **swww** on **Hyprland**, with support for different wallpapers on each monitor.

## Installation

### Using pipx (Python)

```bash
git clone https://github.com/nevimmu/wallpaper-maid
cd wallpaper-maid
pipx install .

wallpaper-maid -s # To setup the tool
```

### NixOS home-manager

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    wallpaper-maid = {
      url = "github:nevimmu/wallpaper-maid";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { nixpkgs, home-manager, wallpaper-maid, ... }: {
    homeConfigurations."your-username" = home-manager.lib.homeManagerConfiguration {
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      modules = [
        wallpaper-maid.homeManagerModules.default
        {
          programs.wallpaper-maid = {
            enable = true;
            wallpapersDirectory = "/home/your-username/Pictures/Wallpapers";
            
            # Optional: Custom theme configuration
            theme = {
              enable = true;
              font = "JetBrains Mono Nerd Font 18";
              backgroundColor = "rgba(30, 30, 46, 0.8)";
              selectedBackgroundColor = "rgba(137, 180, 250, 0.8)";
              iconSize = "250px";
            };
            
            # Optional: Pre-configure monitors
            monitors = {
              "DP-1" = { suffix = "main"; fps = 144; };
              "HDMI-A-1" = { suffix = "left"; fps = 60; };
            };
          };
        }
      ];
    };
  };
}
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
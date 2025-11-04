{
  description = "Wallpaper-maid: A script to set your wallpaper using rofi and swww on Hyprland";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        wallpaper-maid = pkgs.python3Packages.buildPythonApplication rec {
          pname = "wallpaper-maid";
          version = "0.3.0";
          format = "pyproject";

          src = ./.;

          nativeBuildInputs = with pkgs.python3Packages; [
            setuptools
          ];

          propagatedBuildInputs = with pkgs.python3Packages; [
            argcomplete
            questionary
          ];

          # Runtime dependencies (these need to be available in PATH)
          buildInputs = with pkgs; [
            rofi
            swww
          ];

          # Ensure runtime dependencies are available
          makeWrapperArgs = [
            "--prefix PATH : ${pkgs.lib.makeBinPath [ pkgs.rofi pkgs.swww ]}"
          ];

          # Tests are not present in the repository
          doCheck = false;

          meta = with pkgs.lib; {
            description = "Wallpaper-maid help with your wallpapers";
            homepage = "https://github.com/nevimmu/wallpaper-maid";
            license = licenses.mit;
            maintainers = [ ];
            platforms = platforms.linux;
          };
        };

      in {
        packages = {
          default = wallpaper-maid;
          wallpaper-maid = wallpaper-maid;
        };

        apps.default = flake-utils.lib.mkApp {
          drv = wallpaper-maid;
          name = "wallpaper-maid";
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            python3Packages.setuptools
            python3Packages.argcomplete
            python3Packages.questionary
            rofi
            swww
          ];
        };
      }) // {
        # Home Manager module
        homeManagerModules.default = { config, lib, pkgs, ... }:
          with lib;
          let
            cfg = config.programs.wallpaper-maid;
            wallpaper-maid-pkg = self.packages.${pkgs.system}.wallpaper-maid;
          in {
            options.programs.wallpaper-maid = {
              enable = mkEnableOption "wallpaper-maid";

              package = mkOption {
                type = types.package;
                default = wallpaper-maid-pkg;
                description = "The wallpaper-maid package to use.";
              };

              wallpapersDirectory = mkOption {
                type = types.str;
                default = "${config.home.homeDirectory}/Pictures/Wallpapers";
                description = "Directory containing wallpapers.";
              };

              theme = {
                enable = mkOption {
                  type = types.bool;
                  default = true;
                  description = "Enable custom rofi theme for wallpaper-maid.";
                };
                
                font = mkOption {
                  type = types.str;
                  default = "CartographCF Nerd Font 20";
                  description = "Font to use in the rofi theme.";
                };

                backgroundColor = mkOption {
                  type = types.str;
                  default = "rgba(0, 0, 0, 0.27)";
                  description = "Background color for the rofi window.";
                };

                selectedBackgroundColor = mkOption {
                  type = types.str;
                  default = "rgba(185, 185, 185, 0.27)";
                  description = "Background color for selected items.";
                };

                iconSize = mkOption {
                  type = types.str;
                  default = "300px";
                  description = "Size of wallpaper icons.";
                };

                borderRadius = mkOption {
                  type = types.str;
                  default = "20px 20px 0px 0px";
                  description = "Border radius for the rofi window.";
                };
              };

              monitors = mkOption {
                type = types.attrsOf (types.submodule {
                  options = {
                    suffix = mkOption {
                      type = types.str;
                      description = "Suffix for wallpapers on this monitor (e.g., 'main', 'left', 'right').";
                    };
                    fps = mkOption {
                      type = types.int;
                      default = 60;
                      description = "Refresh rate for wallpaper transitions on this monitor.";
                    };
                  };
                });
                default = {};
                example = {
                  "DP-1" = {
                    suffix = "main";
                    fps = 144;
                  };
                  "HDMI-A-1" = {
                    suffix = "left";
                    fps = 60;
                  };
                };
                description = "Monitor configuration for wallpaper-maid.";
              };
            };

            config = mkIf cfg.enable {
              home.packages = [ cfg.package ];

              # Create the wallpapers directory if it doesn't exist
              home.file."${removePrefix config.home.homeDirectory cfg.wallpapersDirectory}/.keep".text = "";

              # Install custom rofi theme if enabled
              xdg.configFile."wallpaper-maid/theme.rasi" = mkIf cfg.theme.enable {
                text = ''
                  configuration {
                    font: "${cfg.theme.font}";
                  }

                  * {
                    background: transparent;
                    foreground: white;
                  }

                  window {
                    width: 80%;
                    background-color: ${cfg.theme.backgroundColor};
                    border: 0px;
                    location: south;
                    anchor: south;
                    border-radius: ${cfg.theme.borderRadius};
                  }

                  listview {
                    spacing: 0px;
                    scrollbar: false;
                    layout: horizontal;
                    
                    background-color: transparent;
                  }

                  element {
                    orientation: vertical;
                    background-color: transparent;
                  }

                  element alternate.normal,
                  element selected.normal {
                    background-color: transparent;
                    text-color: white;
                  }

                  element selected.normal {
                    background-color: ${cfg.theme.selectedBackgroundColor};
                    text-color: white;
                  }

                  element-icon {
                    size: ${cfg.theme.iconSize};
                    expand: true;
                    background-color: transparent;
                  }

                  element-text {
                    horizontal-align: 0.5;
                  }
                '';
              };

              # Create wallpaper-maid configuration
              xdg.configFile."wallpaper-maid/wallpaper-maid.json" = mkIf (cfg.monitors != {}) {
                text = builtins.toJSON {
                  wallpapers_dir = cfg.wallpapersDirectory;
                  screens = cfg.monitors;
                };
              };
            };
          };
      };
}
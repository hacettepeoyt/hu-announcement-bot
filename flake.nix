{
  description = "Get the latest from Hacettepe with this amazing Telegram Bot!";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
  };

  outputs = { self, nixpkgs }:
  let
    forAllSystems = nixpkgs.lib.genAttrs [ "aarch64-linux" "x86_64-linux" ];
  in {
    packages = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      default = self.packages.${system}.hu-announcement-bot;

      hu-announcement-bot = pkgs.stdenv.mkDerivation {
        pname = "hu-announcement-bot";
        version = "3.8.0";
        src = ./.;

        buildInputs = with pkgs; [
          python3Packages.aiohttp
          python3Packages.beautifulsoup4
          python3Packages.dnspython
          python3Packages.lxml
          python3Packages.motor
          python3Packages.python-telegram-bot
          python3Packages.toml
        ]
        ++ python3Packages.python-telegram-bot.optional-dependencies.job-queue
        ++ python3Packages.python-telegram-bot.optional-dependencies.webhooks;

        dontBuild = true;

        installPhase = ''
          mkdir -p $out/{bin,lib/hu-announcement-bot}

          cp -r ./* $out/lib/hu-announcement-bot
          mv $out/lib/hu-announcement-bot/{src,hu-announcement-bot}
          cat <<EOF > $out/bin/hu-announcement-bot
          #!/bin/sh
          PYTHONPATH="$out/lib/hu-announcement-bot:$PYTHONPATH" exec ${pkgs.python3.interpreter} -m hu-announcement-bot "\$@"
          EOF
          chmod +x $out/bin/hu-announcement-bot
        '';
      };
    });

    nixosModules = { lib, config, pkgs, ... }: let
      cfg = config.services.hu-announcement-bot;
      configFormat = pkgs.formats.toml { };
      configFile = configFormat.generate "hu-announcement-bot.toml" cfg.settings;
    in {
      options.services.hu-announcement-bot = {
        enable = lib.mkEnableOption "hu-announcement-bot";

        environmentFile = lib.mkOption {
          type = lib.types.nullOr lib.types.path;
          example = "/run/agenix/x-config.env";
          default = null;
          description = ''Environment file for providing secrets to the unit.'';
        };

        hostname = lib.mkOption {
          type = lib.types.nullOr lib.types.str;
          example = "huannouncementbot.example.org";
          default = null;
          description = "Domain of the host for the webhook. Will enable the webhook and an NGINX virtual host for it.";
        };

        settings = lib.mkOption {
          type = lib.types.submodule {
            freeformType = configFormat.type;
            options = {
                TELEGRAM_API_KEY = lib.mkOption {
                  type = lib.types.str;
                  description = "The telegram token fetched from BotFather.";
                };
                DB_STRING = lib.mkOption {
                  type = lib.types.str;
                  description = "The database URI string for mongodb.";
                };
                DB_NAME = lib.mkOption {
                  type = lib.types.str;
                  description = "The name of the database.";
                };
                ADMIN_ID = lib.mkOption {
                  type = lib.types.int;
                  description = "The ID of the room for admin operations.";
                };
                FEEDBACK_CHAT_ID = lib.mkOption {
                  type = lib.types.int;
                  description = "The ID of the room to send feedback messages to. Defaults to ADMIN_ID.";
                  default = cfg.settings.ADMIN_ID;
                };
                LOGGER_CHAT_ID = lib.mkOption {
                  type = lib.types.int;
                  description = "The ID of the room to send log messages to. Defaults to ADMIN_ID.";
                  default = cfg.settings.ADMIN_ID;
                };
                DEFAULT_DEPS = lib.mkOption {
                  type = lib.types.listOf lib.types.str;
                  description = "The list of departments to be subscribed by default.";
                  default = [];
                };
                ANNOUNCEMENT_CHECK_INTERVAL = lib.mkOption {
                  type = lib.types.int;
                  default = 1800;
                  description = "The interval between subsequent announcement scrapings in seconds.";
                };
                ANNOUNCEMENT_CHECK_FIRST = lib.mkOption {
                  type = lib.types.int;
                  default = 5;
                  description = "The delay before the initial announcement scraping on bot startup in seconds.";
                };
                WEBHOOK_CONNECTED = lib.mkOption {
                  type = lib.types.bool;
                  default = cfg.hostname != null;
                  description = "Whether to use webhook instead of polling for messages. Defaults to true if `services.hu-announcement-bot.hostname` is non-null.";
                };
                PORT = lib.mkOption {
                  type = lib.types.port;
                  default = 31415;
                  description = "The port to listen the webhook on.";
                };
                WEBHOOK_URL = lib.mkOption {
                  type = lib.types.str;
                  default = "https://${cfg.hostname}";
                  description = "The URL for the webhook. Defaults to hostname.";
                };
                FEEDBACK_TIMEOUT = lib.mkOption {
                  type = lib.types.int;
                  default = 300;
                  description = "The timeout for bot to stop listening to a user's feedback message in seconds.";
                };
                ADMIN_ANNOUNCEMENT_TIMEOUT = lib.mkOption {
                  type = lib.types.int;
                  default = 300;
                  description = "The timeout for bot to stop listening to an admin's announcement message in seconds.";
                };
                ADD_TIMEOUT = lib.mkOption {
                  type = lib.types.int;
                  default = 60;
                  description = "The timeout for a user to pick a department to add in seconds.";
                };
                REMOVE_TIMEOUT = lib.mkOption {
                  type = lib.types.int;
                  default = 60;
                  description = "The timeout for a user to pick a department to remove in seconds.";
                };
                DEFAULT_LANGUAGE = lib.mkOption {
                  type = lib.types.enum [ "en" "tr" "fr" ];
                  default = "en";
                  description = "The default language for new users.";
                };
            };
          };
          default = { };
        };
      };

      config = lib.mkIf cfg.enable {
        services.nginx = lib.mkIf (cfg.hostname != null) {
          enable = lib.mkDefault true;

          recommendedGzipSettings = lib.mkDefault true;
          recommendedProxySettings = lib.mkDefault true;

          virtualHosts.${cfg.hostname} = {
            forceSSL = lib.mkDefault true;
            enableACME = lib.mkDefault true;

            locations."/".proxyPass = "http://localhost:${toString cfg.settings.PORT}";
          };
        };

        systemd.services.hu-announcement-bot = {
          enable = true;
          wantedBy = [ "multi-user.target" ];
          after = [ "network.target" ];
          startLimitBurst = 3;
          startLimitIntervalSec = 60;

          serviceConfig = {
            ExecStart = "${self.packages.${pkgs.system}.hu-announcement-bot}/bin/hu-announcement-bot /run/hu-announcement-bot/hu-announcement-bot.toml";
            ExecStartPre = ''
                ${pkgs.envsubst}/bin/envsubst -i ${configFile} -o /run/hu-announcement-bot/hu-announcement-bot.toml
            '';
            EnvironmentFile = lib.mkIf (cfg.environmentFile != null) cfg.environmentFile;

            Type = "simple";
            Restart = "always";
            DynamicUser = true;
            User = "hu-announcement-bot";
            Group = "hu-announcement-bot";
            RuntimeDirectory = "hu-announcement-bot";
            RuntimeDirectoryMode = "0700";
            StateDirectory = "hu-announcement-bot";
            WorkingDirectory = "${self.packages.${pkgs.system}.hu-announcement-bot}/lib/hu-announcement-bot";

            LockPersonality = true;
            PrivateDevices = true;
            PrivateTmp = true;
            PrivateUsers = true;
            ProtectClock = true;
            ProtectControlGroups = true;
            ProtectHome = true;
            ProtectHostname = true;
            ProtectKernelLogs = true;
            ProtectKernelModules = true;
            ProtectKernelTunables = true;
            ProtectProc = "invisible";
            RestrictNamespaces = true;
            RestrictRealtime = true;
            RestrictSUIDSGID = true;
            SystemCallArchitectures = "native";
            UMask = "0007";
          };
        };
      };
    };
  };
}

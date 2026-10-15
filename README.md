# moicpl.app_config

The state of the apps running in lab1's NixOS containers, as code: what the
containers of [moicpl.nixos](https://github.com/moicpl/collection-nixos) run
(logins, settings, cameras, series...). These playbooks never change the
containers themselves.

Run through [nixos_playbooks](https://github.com/moicpl/nixos_playbooks)
(`ansible-playbook config/<app>.yml -e app_action=<action>`), which holds the
inventory link, `ansible.cfg` and the app state store link.

## Playbooks

Each takes `app_action`:

- `configure`: sets the app to the state in the inventory
  (`inventory/group_vars/<group>/<app>.yml`)
- `backup`: saves the live state in the app state store
  (`appstate/<host>/<app>/`) and shows its drift from the inventory
- `default`: factory reset with only the admin login; needs `-e app_wipe=true`,
  and keeps a snapshot on the host first

| Playbook | Hosts | Role |
| --- | --- | --- |
| `moicpl.app_config.frigate` | `nixos_home` | `moicpl.app_config.frigate`: config.yaml, camera and admin passwords |
| `moicpl.app_config.sonarr` | `nixos_arr` | `moicpl.app_config.sonarr`: login, root folders, series, download clients |
| `moicpl.app_config.prowlarr` | `nixos_arr` | `moicpl.app_config.prowlarr`: login |

## Requirements

- `moicpl.nixos` (login to the hosts, `connect.yml` of its `nixos` role) and
  `community.sops` (Frigate's encrypted backups).
- The `bitwarden` role (https://github.com/moicpl/bitwarden) in the roles path:
  it isn't a collection, so it is not a galaxy dependency; nixos_playbooks
  clones and links it.
- `appstate_dir` (the app state store) and, for Frigate, the store's age key
  (`appstate_age_public_key` in the inventory, `appstate_age_key` in Bitwarden,
  from nixos_playbooks/appstate_key.yml).

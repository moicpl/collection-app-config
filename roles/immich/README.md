# immich

Manages the state of an [Immich](https://immich.app) server
(`podman-<immich_container>.service` and its database containers, set up by
moicpl.nixos.arr_nix) through its API. The playbook (moicpl.app_config.immich)
reads the admin password from Bitwarden and passes it in.

| `immich_action` | What it does |
| --- | --- |
| `configure` | On the first start, creates the admin user (`immich_admin_email` / `immich_admin_password`). Logs in and sets the settings: Immich's defaults with `immich_system_config` merged in, so settings changed in the UI and not in the variables go back to their defaults. |
| `backup` | Saves the admin user and the settings that differ from Immich's defaults as `immich.yml` in `immich_store_dir`, in the format of the variables, and shows its diff from the variables: changes made in Immich's UI. |
| `user` | Creates a user that isn't an admin (`immich_user_login`, its email, `immich_user_name`, `immich_user_password`) when Immich has none with that email. An existing one is left alone, its password too. |
| `default` | With `immich_wipe: true`: stops Immich, keeps a snapshot of its database on the host (`immich_snapshot_dir`), erases it, and starts Immich empty with the admin user only. The photo files stay on `/data`, unknown to the new database. |

Immich changes a password only given the current one: when the password in
Bitwarden doesn't log in, configure stops and says how to reset it. Not
managed: other users once created (their passwords, roles), albums, libraries (they are data, in the database).

The `moicpl.app_config.dict_changes` filter keeps the settings that differ
from the defaults; `dict_unknown_keys` catches a misspelled setting.

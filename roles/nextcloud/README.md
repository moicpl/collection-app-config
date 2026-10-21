# nextcloud

Manages the state of a [Nextcloud](https://nextcloud.com) server
(`podman-<nextcloud_container>.service`, its cron, PostgreSQL and Redis
containers, set up by moicpl.nixos.arr_nix) with `occ` in the container. The
playbook (moicpl.app_config.nextcloud) reads the admin and database passwords
from Bitwarden and passes them in.

| `nextcloud_action` | What it does |
| --- | --- |
| `configure` | On the first start, restores the database and `config.php` saved by `backup` when the store has them (then upgrades the database if the image is newer and rescans the users' files), or else installs Nextcloud (PostgreSQL, data in `nextcloud_data_mount`, i.e. `nextcloud_data_dir` on the host) with the admin user. Sets the admin password back when it doesn't log in, sets the settings that differ (`nextcloud_system_config` for config.php, `nextcloud_app_config` for the apps, plus the trusted domains, the CLI URL and cron background jobs), and installs, enables and disables the apps (`nextcloud_apps_enabled`, `nextcloud_apps_disabled`). |
| `backup` | Saves the database (`database.sql.gz.sops`, `pg_dump`), Nextcloud's database role (`roles.sql.sops`) and `config.php` (`config.php.sops`) in `nextcloud_store_dir`, encrypted with sops to `nextcloud_age_recipient` and rewritten only when they changed. Saves the live values of the listed settings, the state of the listed apps and the app store apps enabled as `nextcloud.yml` in `nextcloud_store_dir`, in the format of the variables, and shows its diff from the variables: changes made in Nextcloud's UI. |
| `user` | Creates a user outside the admin group (`nextcloud_user_login` / `nextcloud_user_password`, which Nextcloud's password policy may refuse) when Nextcloud has none with that name. An existing one is left alone, its password too. |
| `default` | With `nextcloud_wipe: true`: stops Nextcloud, keeps a snapshot of its config and database on the host (`nextcloud_snapshot_dir`), erases them, renames the data directory to `<dir>.<date>` (kept), and installs Nextcloud again with the admin user only. |

The settings not listed are left alone. The users' files are on `/data` (the
NAS), not in the store: backup saves what Nextcloud knows about them (users,
shares, calendars, contacts, the file cache), which a restore rescans.
Encryption and decryption happen in memory on the controller, which needs
`sops` and the `community.sops` collection. A large database goes through
the controller's memory.

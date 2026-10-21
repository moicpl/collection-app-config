# jellyfin

Manages the state of a [Jellyfin](https://jellyfin.org) container
(`podman-<jellyfin_container>.service`, set up by moicpl.nixos.arr_nix)
through its API. The playbook (moicpl.app_config.jellyfin) reads the admin
password from Bitwarden and passes it in.

| `jellyfin_action` | What it does |
| --- | --- |
| `configure` | On the first start, runs the wizard and creates the admin user (`jellyfin_admin_username` / `jellyfin_admin_password`). Logs in, adds the missing libraries (`jellyfin_libraries`, by name) and library paths, and sets the server and transcoding settings that differ (`jellyfin_server_config`, `jellyfin_encoding_config`). |
| `backup` | Saves the admin user, the libraries and the live values of the listed settings as `jellyfin.yml` in `jellyfin_store_dir`, in the format of the variables, and shows its diff from the variables: changes made in Jellyfin's UI. |
| `user` | Creates a user that isn't an administrator (`jellyfin_user_login` / `jellyfin_user_password`), with access to all the libraries, when Jellyfin has none with that name. An existing one is left alone, its password too. |
| `default` | With `jellyfin_wipe: true`: stops Jellyfin, keeps a snapshot on the host (`jellyfin_snapshot_dir`), erases its config and database (not the media), and starts it empty with the admin user only. |

Jellyfin changes a password only given the current one: when the password in
Bitwarden doesn't log in, configure stops and says so. Libraries and paths in
Jellyfin but not in the variables are left alone, and reported; a library's
type can't change. Not managed: other users once created (their passwords, access), plugins, the settings not listed.

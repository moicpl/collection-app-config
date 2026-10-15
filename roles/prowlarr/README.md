# prowlarr

Manages the state of a [Prowlarr](https://prowlarr.com) container
(`podman-<prowlarr_container>.service`, set up by moicpl.nixos.arr_nix)
through its API. The playbook (moicpl.app_config.prowlarr) reads the
login password from Bitwarden and passes it in.

| `prowlarr_action` | What it does |
| --- | --- |
| `configure` | Sets the login (forms, `prowlarr_admin_username` / `prowlarr_admin_password`; Prowlarr restarts when it changes). |
| `backup` | Saves the live login user and where the login is required as `prowlarr.yml` in `prowlarr_store_dir`, in the format of the variables, and shows its diff from the variables: changes made in Prowlarr's UI. |
| `default` | With `prowlarr_wipe: true`: stops Prowlarr, keeps a snapshot on the host (`prowlarr_snapshot_dir`), erases its config and database, and starts it empty with the login only. |

Not managed yet: indexers, apps (Sonarr, Radarr, Lidarr), download clients and
the other settings.

The API key is read from Prowlarr's `config.xml` on the host; the API calls are
made from the host to `prowlarr_url`.

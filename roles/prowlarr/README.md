# prowlarr

Manages the state of a [Prowlarr](https://prowlarr.com) container
(`podman-<prowlarr_container>.service`, set up by moicpl.nixos.arr_nix)
through its API. The playbook (moicpl.app_config.prowlarr) reads the
login password from Bitwarden and passes it in.

| `prowlarr_action` | What it does |
| --- | --- |
| `configure` | Sets the login (forms, `prowlarr_admin_username` / `prowlarr_admin_password`; Prowlarr restarts when it changes), and adds or updates the apps Prowlarr syncs its indexers to (`prowlarr_applications`, by name: Sonarr, Radarr, Lidarr...). |
| `backup` | Saves the live login user, where the login is required and the apps as `prowlarr.yml` in `prowlarr_store_dir`, in the format of the variables, and shows its diff from the variables: changes made in Prowlarr's UI. |
| `default` | With `prowlarr_wipe: true`: stops Prowlarr, keeps a snapshot on the host (`prowlarr_snapshot_dir`), erases its config and database, and starts it empty with the login only. |

Apps are only added or updated: those in Prowlarr but not in the variables
are left alone, and reported. Each app's API key is read from its own
`config.xml` on the host (`/var/lib/<app>`), so the app must have started
once; Prowlarr tests the connection to the app before it saves it. Not managed
yet: indexers, download clients and the other settings.

The API key is read from Prowlarr's `config.xml` on the host; the API calls are
made from the host to `prowlarr_url`.

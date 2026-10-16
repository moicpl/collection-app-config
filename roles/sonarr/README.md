# sonarr

Manages the state of a [Sonarr](https://sonarr.tv) container
(`podman-<sonarr_container>.service`, set up by moicpl.nixos.arr_nix)
through its API. The playbook (moicpl.app_config.sonarr) reads the
login password from Bitwarden and passes it in.

| `sonarr_action` | What it does |
| --- | --- |
| `configure` | Sets the login (forms, `sonarr_admin_username` / `sonarr_admin_password`; Sonarr restarts when it changes), adds the missing root folders and series (`sonarr_series`, by TVDB ID), puts back the quality profile, monitored and season folder settings of the listed series, and adds or updates the download clients (`sonarr_download_clients`, by name). |
| `backup` | Saves the live login user, root folders, series and download clients as `sonarr.yml` in `sonarr_store_dir`, in the format of the variables, and shows its diff from the variables: changes made in Sonarr's UI. |
| `default` | With `sonarr_wipe: true`: stops Sonarr, keeps a snapshot on the host (`sonarr_snapshot_dir`), erases its config and database (not the media), and starts it empty with the login only. |

Series, root folders and download clients are only added or updated: those
in Sonarr but not in the variables are left alone, and reported. A download
client's password comes from Bitwarden (its `password_secret`); such a client
is tested at each run and updated when the test fails. Not managed yet:
indexers (Prowlarr pushes them), quality profiles and the other settings.

The API key is read from Sonarr's `config.xml` on the host; the API calls are
made from the host to `sonarr_url`.

# radarr

Manages the state of a [Radarr](https://radarr.video) container
(`podman-<radarr_container>.service`, set up by moicpl.nixos.arr_nix)
through its API. The playbook (moicpl.app_config.radarr) reads the
login password from Bitwarden and passes it in.

| `radarr_action` | What it does |
| --- | --- |
| `configure` | Sets the login (forms, `radarr_admin_username` / `radarr_admin_password`; Radarr restarts when it changes), adds the missing root folders and movies (`radarr_movies`, by TMDB ID), puts back the quality profile, monitored and minimum availability settings of the listed movies, and adds or updates the download clients (`radarr_download_clients`, by name). |
| `backup` | Saves the live login user, root folders, movies and download clients as `radarr.yml` in `radarr_store_dir`, in the format of the variables, and shows its diff from the variables: changes made in Radarr's UI. |
| `default` | With `radarr_wipe: true`: stops Radarr, keeps a snapshot on the host (`radarr_snapshot_dir`), erases its config and database (not the media), and starts it empty with the login only. |

Movies, root folders and download clients are only added or updated: those
in Radarr but not in the variables are left alone, and reported. A download
client's password comes from Bitwarden (its `password_secret`); such a client
is tested at each run and updated when the test fails. Not managed yet:
indexers (Prowlarr pushes them), quality profiles and the other settings.

The API key is read from Radarr's `config.xml` on the host; the API calls are
made from the host to `radarr_url`.

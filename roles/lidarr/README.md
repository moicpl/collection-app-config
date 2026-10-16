# lidarr

Manages the state of a [Lidarr](https://lidarr.audio) container
(`podman-<lidarr_container>.service`, set up by moicpl.nixos.arr_nix)
through its API. The playbook (moicpl.app_config.lidarr) reads the
login password from Bitwarden and passes it in.

| `lidarr_action` | What it does |
| --- | --- |
| `configure` | Sets the login (forms, `lidarr_admin_username` / `lidarr_admin_password`; Lidarr restarts when it changes), adds the missing root folders (with default profiles) and artists (`lidarr_artists`, by MusicBrainz ID), puts back the quality profile, metadata profile and monitored settings of the listed artists, and adds or updates the download clients (`lidarr_download_clients`, by name). |
| `backup` | Saves the live login user, root folders, artists and download clients as `lidarr.yml` in `lidarr_store_dir`, in the format of the variables, and shows its diff from the variables: changes made in Lidarr's UI. |
| `default` | With `lidarr_wipe: true`: stops Lidarr, keeps a snapshot on the host (`lidarr_snapshot_dir`), erases its config and database (not the media), and starts it empty with the login only. |

Artists, root folders and download clients are only added or updated: those
in Lidarr but not in the variables are left alone, and reported. Download
client passwords aren't set. Not managed yet: indexers (Prowlarr pushes them),
quality profiles and the other settings.

The API key is read from Lidarr's `config.xml` on the host; the API calls are
made from the host to `lidarr_url`.

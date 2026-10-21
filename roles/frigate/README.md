# frigate

Manages the state of a [Frigate](https://frigate.video) NVR that runs as a podman
container (`podman-<frigate_container>.service`, set up by
moicpl.nixos.home_management). Frigate's config is fully declarative,
so the role builds `config.yaml` from variables. The playbook
(moicpl.app_config.frigate) reads the passwords from Bitwarden and
passes them in.

| `frigate_action` | What it does |
| --- | --- |
| `configure` | Writes the camera and restream passwords as `FRIGATE_*` files in the container's `/run/secrets` and `config.yaml` from the variables (checked by Frigate before it is installed), restarts Frigate when one changed, and sets the admin password. |
| `backup` | Saves the running `config.yaml` in `frigate_store_dir`, encrypted with sops (age), and shows its diff from the variables: changes made in Frigate's UI, which the next `configure` replaces. |
| `user` | Creates a viewer user (`frigate_user_login` / `frigate_user_password`) in Frigate's database when it has none with that name. An existing one is left alone, its password too. |
| `default` | With `frigate_wipe: true`: stops Frigate, keeps a snapshot on the host (`frigate_snapshot_dir`), erases its config, database and passwords (and recordings with `frigate_wipe_media`), and starts it empty with the admin password. |

Cameras are described in `frigate_cameras` (see `defaults/main.yml`). Each one's
streams go through go2rtc, whose RTSP restream (port 8554) requires
`frigate_restream_username` / `frigate_restream_password`. Passwords never
appear in `config.yaml`: it uses `{FRIGATE_*}` placeholders, which Frigate fills
from `/run/secrets`.

The admin password is written in Frigate's database (`files/user_password.py`,
same hash as Frigate) because Frigate has no setting for it.

Requires the `community.sops` collection and `sops` on the controller.

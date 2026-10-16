# transmission

Manages the state of a [Transmission](https://transmissionbt.com) container
(`podman-<transmission_container>.service`, haugene/transmission-openvpn, set
up by moicpl.nixos.arr_nix) through its RPC API.

| `transmission_action` | What it does |
| --- | --- |
| `configure` | Sets the session settings of `transmission_settings` (RPC names: `speed-limit-down`, `seedRatioLimit`...) that differ. Transmission saves them in its `settings.json`. |
| `backup` | Saves the live values of those settings as `transmission.yml` in `transmission_store_dir`, in the format of the variables, and shows its diff from the variables: changes made in Transmission's UI. |
| `default` | With `transmission_wipe: true`: stops Transmission, keeps a snapshot on the host (`transmission_snapshot_dir`), erases its state (settings, torrent list), not the downloads, and starts it again with the settings of its container environment. |

The download paths, the RPC whitelist and the login come from the container's
environment (arr_nix.yml), which overrides `settings.json` at each start: they
aren't set here. The role logs in with `transmission_rpc_username` and
`transmission_rpc_password` (Bitwarden, created by arr_nix.yml), as do the
*arr apps' download clients.

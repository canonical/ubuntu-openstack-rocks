# ovs-cni-plugin ROCK

This is a ROCK OCI image for ovs-cni-plugin, built from
[hemanthnakkina/ovs-cni](https://github.com/hemanthnakkina/ovs-cni) branch
`args-cni-ovnport`.

It contains the following binaries (all at the image root to match the upstream
[ovs-cni.yml.in](https://github.com/hemanthnakkina/ovs-cni/blob/main/manifests/ovs-cni.yml.in)
manifest):
- `/ovs` — Main OVS CNI plugin. Copied by an init container to the CNI bin path
  on the host. Adds and removes OVS bridge interfaces with OVN port argument support.
- `/marker` — OVS marker daemon. Runs as the main DaemonSet container; annotates
  nodes with OVS bridge availability.
- `/ovs-mirror-producer` — Mirror producer binary, also copied by the init container.
- `/ovs-mirror-consumer` — Mirror consumer binary, also copied by the init container.

If you want to play with it:

```bash
> sudo snap install rockcraft --edge --classic
> rockcraft pack
```

Now that you have created the ROCK, you can import it into
your local docker repository. Using skopeo is a good idea as
it will help ensure that all layers of the image are imported
into docker (this is just the top layer).

```bash
> skopeo --insecure-policy copy oci-archive:ovs-cni-plugin_0.1.0-107d5dd_amd64.rock docker-daemon:ovs-cni-plugin:0.1.0-107d5dd
```

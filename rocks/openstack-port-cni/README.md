# openstack-port-cni ROCK

This is a ROCK OCI image for openstack-port-cni.

It contains two binaries:
- `openstack-port-cni` — Thin CNI binary installed at `/opt/cni/bin/openstack-port-cni`. Typically copied to the host via an init container. Invoked by kubelet, talks to the daemon over a Unix socket, then delegates to OVS CNI.
- `openstack-port-daemon` — Thick daemon binary at `/usr/bin/openstack-port-daemon`. Runs as a DaemonSet, holds OpenStack credentials, manages Neutron ports.

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
> skopeo --insecure-policy copy oci-archive:openstack-port-cni_0.1.0-7e56263_amd64.rock docker-daemon:openstack-port-cni:0.1.0-7e56263
```

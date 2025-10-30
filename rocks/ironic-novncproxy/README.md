# ironic-novncproxy ROCK

This is a ROCK OCI image for ironic-novncproxy.

More information is coming.

For now, if you want to play with it:

```bash
> sudo snap install rockcraft --edge --classic
> rockcraft pack
```

Now that you have created the ROCK, you can import it into
your local docker repository. Using skopeo is a good idea as
it will help ensure that all layers of the image are imported
into docker (this is just the top layer).

```bash
> skopeo --insecure-policy copy oci-archive:ironic-novncproxy_2024.1_amd64.rock docker-daemon:ironic-novncproxy:2024.1
```

If you are interested in giving it a go in Microk8s, you can
export the image from your docker registry and then into the
microk8s registry:

```bash
> docker save ironic-novncproxy:2024.1 > ./ironic-novncproxy_2024.1.tar
> microk8s ctr image import ./ironic-novncproxy_2024.1.tar
# Try with sunbeam
> /snap/k8s/current/bin/ctr --namespace k8s.io image import ./ironic-novncproxy_2024.1.tar
> juju attach-resource ironic ironic-novncproxy-image=ironic-novncproxy:2024.1
```

# watcher-applier ROCK

This is a ROCK OCI image for watcher-applier.

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
> skopeo --insecure-policy copy oci-archive:watcher-applier_2024.2_amd64.rock docker-daemon:watcher-applier:2024.2
```

If you are interested in giving it a go in Microk8s, you can
export the image from your docker registry and then into the
microk8s registry:

```bash
> docker save watcher-applier:2024.2 > ./watcher-applier_2024.2.tar
> microk8s ctr image import ./watcher-applier_2024.2.tar
# Try with sunbeam
> juju attach-resource watcher-k8s watcher-applier-image=watcher-applier:2024.2
```

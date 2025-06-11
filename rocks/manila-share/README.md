# manila-share ROCK

This is a ROCK OCI image for manila-share.

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
> skopeo --insecure-policy copy oci-archive:manila-share_2025.1_amd64.rock docker-daemon:manila-share:2025.1
```

If you are interested in giving it a go in Microk8s, you can
export the image from your docker registry and then into the
microk8s registry:

```bash
> docker save manila-share:2025.1 > ./manila-share_2025.1.tar
> microk8s ctr image import ./manila-share_2025.1.tar
# Try with sunbeam
> /snap/k8s/current/bin/ctr --namespace k8s.io image import ./manila-share_2025.1.tar
> juju attach-resource manila-share manila-share-image=manila-share:2025.1
```

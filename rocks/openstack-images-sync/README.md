# openstack-images-sync ROCK

This is a ROCK OCI image for openstack-images-sync.

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
> skopeo --insecure-policy copy oci-archive:openstack-images-sync_2024.1_amd64.rock docker-daemon:openstack-images-sync:2024.1
```

If you are interested in giving it a go in Microk8s, you can
export the image from your docker registry and then into the
microk8s registry:

```bash
> docker save openstack-images-sync:2024.1 > ./openstack-images-sync_2024.1.tar
> microk8s ctr image import ./openstack-images-sync_2024.1.tar
# Try with sunbeam
> juju attach-resource openstack-images-sync openstack-images-sync-image=openstack-images-sync:2024.1
```

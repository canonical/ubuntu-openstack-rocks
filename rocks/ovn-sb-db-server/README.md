# ovn-sb-db-server ROCK

This is a ROCK OCI image for ovn-sb-db-server.

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
> skopeo --insecure-policy copy oci-archive:ovn-sb-db-server_24.09_amd64.rock docker-daemon:ovn-sb-db-server:24.09
```

If you are interested in giving it a go in Microk8s, you can
export the image from your docker registry and then into the
microk8s registry:

```bash
> docker save ovn-sb-db-server:24.09 > ./ovn-sb-db-server_24.09.tar
> microk8s ctr image import ./ovn-sb-db-server_24.09.tar
# Try with sunbeam
> juju attach-resource ovn-sb-db-server ovn-sb-db-server-image=ovn-sb-db-server:24.09
```

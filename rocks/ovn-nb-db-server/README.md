# ovn-nb-db-server ROCK

This is a ROCK OCI image for ovn-nb-db-server.

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
> skopeo --insecure-policy copy oci-archive:ovn-nb-db-server_25.03_amd64.rock docker-daemon:ovn-nb-db-server:25.03
```

If you are interested in giving it a go in Microk8s, you can
export the image from your docker registry and then into the
microk8s registry:

```bash
> docker save ovn-nb-db-server:25.03 > ./ovn-nb-db-server_25.03.tar
> microk8s ctr image import ./ovn-nb-db-server_25.03.tar
# Try with sunbeam
> juju attach-resource ovn-nb-db-server ovn-nb-db-server-image=ovn-nb-db-server:25.03
```

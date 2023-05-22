# neutron-server ROCK

This is a ROCK OCI image for neutron-server.

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
> skopeo --insecure-policy copy oci-archive:neutron-server_antelope_amd64.rock docker-daemon:neutron-server:antelope
```

If you are interested in giving it a go in Microk8s, you can
export the image from your docker registry and then into the
microk8s registry:

```bash
> docker save neutron-server:antelope > ./neutron-server_antelope.tar
> microk8s ctr image import ./neutron-server_antelope.tar
# Try with sunbeam
> juju attach-resource neutron-server neutron-server-image=neutron-server:antelope
```

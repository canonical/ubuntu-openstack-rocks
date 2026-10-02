# Monolithic repo for OpenStack Rocks

## CI builds

Pushes to the configured branches and manual runs of **Publish all ROCKs from
selected branch** build on Launchpad through `sunbeam-watchtower`. Each ROCK is
built for every architecture declared in its `rockcraft.yaml`. The selected
ROCKs are submitted together in one Watchtower invocation. Successful
Launchpad artifacts are passed to the existing GHCR release workflow. Pull
requests continue to use the GitHub runner build because forked pull requests
do not receive the Launchpad credentials.

The Launchpad build jobs require the `LAUNCHPAD_SSH_PRIVATE_KEY`,
`LP_ACCESS_TOKEN`, and `LP_ACCESS_TOKEN_SECRET` Actions secrets for the
`openstack-ubuntu-testing-bot` Launchpad account. The workflow creates
temporary recipes and Git refs in that account and attempts to remove them
after the release job. Its Watchtower snap channel is set in
`.github/workflows/build_publish.yaml`.

To generate a rock definition from a cookie cutter template:

```bash
> ./rock-init.sh glance-api
> rock_name [glance-api]: 
> packages [sudo nfs-common qemu-utils  glance python3-boto3 python3-os-brick python3-oslo.vmware python3-rados python3-rbd apache2 libapache2-mod-wsgi-py3 openssl]:
```

The output will be in the rocks directory:

```bash
> ls -l rocks/glance-api
> total 20
> -rw-rw-r-- 1 liam liam 10765 May 19 16:59 LICENSE
> -rw-rw-r-- 1 liam liam   913 May 19 16:59 README.md
> -rw-rw-r-- 1 liam liam  1270 May 19 16:59 rockcraft.yaml
```

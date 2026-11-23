# Monolithic repo for OpenStack Rocks

## CI builds

Pushes and manual publishing runs discover the recipes on the selected ref.
A ROCK can declare separate Rockcraft projects by base. For example:

```text
rocks/nova-consolidated/
├── 24.04/rockcraft.yaml
└── 26.04/rockcraft.yaml
```

The directory identifies the Ubuntu runtime base, or the Ubuntu build base for
a `bare` image. Each project contains the local files its recipe needs. To pack
one directly, run `rockcraft pack --platform amd64` in its base directory.

Single-base branches can keep a root recipe at `rocks/<name>/rockcraft.yaml`.
CI builds only the projects that exist on the selected branch. PR checks build
each project from its own directory. Publishing groups builds by base and
copies the selected projects to the ROCK root in temporary Launchpad build
refs, so Watchtower sees one recipe per image name in each build.

Automatic PR and push builds select a ROCK when one of its `rockcraft.yaml`
files changes. Only recipes present on the selected ref enter the build matrix.

Ubuntu images use their usual base-specific tags. For bare images, the Noble
variant uses a `-24.04` version suffix to distinguish its tag from the existing
Resolute-built `-bare_edge` tag. Consul uses `1.19.2-bare_edge` and
`1.19.2-24.04-bare_edge` for the two variants.

For Security Scan and SBOM, select the branch in **Run workflow** so the
reusable build and scan jobs check out the same ref.

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

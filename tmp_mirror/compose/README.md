# how to

## pip

The mirror for pip packages is handled by __bandersnatch__.

### pip mirror config

Change the values in the _bandersnatch.conf_ file or use the more advanced client (banderctl):

```shell
#!/bin/bash
curl -X 'POST' \
  'https://mirror.services.osism.tech/bandermanage/allowlist/packages' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "mode": "add", "packages": ["fastapi"] }'
```

Possible modes: "add", "delete"

### pip mirror update

```shell
#!/bin/bash
docker exec -it pip-bandersnatch-1 bandersnatch -c /conf/bandersnatch.conf mirror
```

But this is (per default) done every hour.

### pip client config

Use the following to fetch python packages from your mirror-host:

```sh
pip install localhost -i https://mirror.services.osism.tech/pypi/foo/simple/ shelf-reader
```

If your mirror installation is not secured with SSL you have to allow this within the command:

```sh
pip install --trusted-host mirror.services.osism.tech -i https://mirror.services.osism.tech/pypi/foo/simple/ shelf-reader
```

Alternatively you can configure your `pip.conf` file:

```ini
[global]
index-url = https://mirror.services.osism.tech/pypi/foo/simple/
#trusted-host = mirror.services.osism.tech  # if no SSL is available
```

## deb

The deb packages mirror is handled by __aptly__.

### deb mirror config

```shell
#!/bin/bash
# docker exec -it deb-aptly-1 /opt/keys_gen.sh "foobar" "foo@bar.com" "123"
# gpg --no-default-keyring --keyring /usr/share/keyrings/debian-archive-keyring.gpg --export | gpg --no-default-keyring --keyring trustedkeys.gpg --import

mirror=webservers
new_snapshot=new_snapshot
old_snapshot=current_snapshot
distribution=bullseye
architectures="amd64,arm64"
packages="nginx | apache2"

docker exec -it deb-aptly-1 aptly mirror create -filter="$packages" -filter-with-deps -architectures=$architectures $mirror http://ftp.de.debian.org/debian/ $distribution main
docker exec -it deb-aptly-1 aptly mirror update $mirror
docker exec -it deb-aptly-1 aptly snapshot create $old_snapshot from mirror $mirror
docker exec -it deb-aptly-1 aptly publish snapshot -architectures=$architectures -distribution=$distribution $old_snapshot $mirror

docker exec -it deb-aptly-1 aptly mirror update $mirror
docker exec -it deb-aptly-1 aptly snapshot create $new_snapshot from mirror $mirror
docker exec -it deb-aptly-1 aptly publish switch $distribution $mirror $new_snapshot
# docker exec -it deb-aptly-1 aptly snapshot drop $old_snapshot
# docker exec -it deb-aptly-1 aptly snapshot rename $new_snapshot $old_snapshot
```

### deb client config

Use the following to fetch deb packages from your mirror-host by configuring `/etc/apt/sources.list` or similar:

```list
deb [trusted=yes arch=amd64,arm64 arch-=i386,armel,armhf] https://mirror.services.osism.tech/deb/ default  all
```

## ansible

The ansible collections and roles mirror is handled by __wormhole__.

### ansible mirror config

Use the wormhole client:

```sh
python3 main.py -r geerlingguy.ansible -r geerlingguy.nginx -c osism.validations -c osism.services
```

### ansible client config

Use the following to pull roles and collections from your wormhole-host:

```sh
ansible-galaxy install elasticsearch,6.2.4 -s https://localhost/
ansible-galaxy collection install 'osism.validations:==0.2.0' -s https://localhost/
```

If your wormhole installation is not secured with SSL you have to allow this within the command:

```sh
ansible-galaxy install elasticsearch,6.2.4 -c -s http://localhost/
ansible-galaxy collection install 'osism.validations:==0.2.0' -c -s http://localhost/
```

Alternatively you can configure this in the various locations of your `ansible.cfg` file (`~/.ansible.cfg`, `/etc/ansible/ansible.cfg`, `./ansible.cfg`):

```ini
[galaxy]
server_list = wormhole, official
#server=https://galaxy.ansible.com/

[galaxy_server.wormhole]
url=http://localhost
validate_certs=false

[galaxy_server.official]
url=https://galaxy.ansible.com/
```

## container

The container mirror is handled by dockers __registry__ software.

### container mirror config

```sh
docker image tag nginx:latest 81.163.192.223/registry/foo/nginx:latest
docker image push 81.163.192.223/registry/foo/nginx:latest
```

### container client config

Use the following to pull containers from your mirror-host:

```sh
docker pull mirror.services.osism.tech/my-image:latest
docker run -d mirror.services.osism.tech/my-image:latest bash
```

If your mirror installation is not secured with SSL you have to allow this to your container engine. For docker modify (or create first) `/etc/docker/daemon.json`:

```json
{
  "insecure-registries" : ["mirror.services.osism.tech"]
}
```

#!/bin/bash
# docker exec -it deb-aptly-1 /opt/keys_gen.sh "foobar" "foo@bar.com" "123"
# docker exec -it deb-aptly-1 apt update
# docker exec -it deb-aptly-1 apt install -y debian-archive-keyring
# gpg --no-default-keyring --keyring /usr/share/keyrings/debian-archive-keyring.gpg --export | gpg --no-default-keyring --keyring trustedkeys.gpg --import
# gpg --no-default-keyring --keyring trustedkeys.gpg --keyserver pgp.mit.edu --recv-keys D27D666CD88E42B4

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

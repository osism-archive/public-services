import docker


def send_command_to_container(container_name, command):
    client = docker.from_env()
    container = client.containers.get(container_name)
    print(command)
    container.exec_run(command, tty=True)
    return container.status


def main():
    packages = "nginx | apache2"
    mirror = "webservers"
    distribution = "bullseye"
    architectures = "amd64,arm64"
    new_snapshot = "new_snapshot"
    old_snapshot = "old_snapshot"

    send_command_to_container("deb-aptly-1", f"aptly mirror create -filter=\"{packages}\" -filter-with-deps -architectures={architectures} {mirror} http://ftp.de.debian.org/debian/ {distribution} main")
    send_command_to_container("deb-aptly-1", f"aptly mirror update {mirror}")
    send_command_to_container("deb-aptly-1", f"aptly snapshot create {old_snapshot} from mirror {mirror}")
    send_command_to_container("deb-aptly-1", f"aptly publish snapshot -architectures={architectures} -distribution={distribution} {old_snapshot} {mirror}")

    send_command_to_container("deb-aptly-1", f"aptly mirror update {mirror}")
    send_command_to_container("deb-aptly-1", f"aptly snapshot create {new_snapshot} from mirror {mirror}")
    send_command_to_container("deb-aptly-1", f"aptly publish switch {distribution} {mirror} {new_snapshot}")
#    send_command_to_container("deb-aptly-1", f"aptly snapshot drop {old_snapshot}")
#    send_command_to_container("deb-aptly-1", f"aptly snapshot rename {new_snapshot} {old_snapshot}")


if __name__ == "__main__":
    main()

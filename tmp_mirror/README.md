# mirror

<https://github.com/osism/tasks/issues/17>

|ecosystem|tool        |further information                               |
|---------|------------|--------------------------------------------------|
|ansible  |wormhole    |<https://github.com/osism/python-ansible-wormhole>|
|container|registry    ||
|deb      |aptly       ||
|pypi     |bandersnatch||

## affected repositories

Hosting mirror services: <https://github.com/osism/public-services>
Providing Helm charts: <https://github.com/osism/helm-charts>
Here should the yaml version files be stored: <https://github.com/osism/sbom>
Here should the yaml mirror files be stored: <https://github.com/osism/sbom>
Here should the scripts be stored that generate the yaml files: <https://github.com/osism/scripts>

## folder structure

_compose_ docker compose of all services to spin up the mirror infrastructure

_helm-charts_ shall hold the contents of compose in helm-charts

_sbom_ yaml file containing all stuff to be mirrored

_scripts_ flanky scripts to fetch all packages of all github repos from all file types

## tasks

- create a helm chart for all services

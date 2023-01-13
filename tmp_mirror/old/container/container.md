# Client config for container mirror

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

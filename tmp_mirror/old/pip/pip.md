# Client config for container mirror

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

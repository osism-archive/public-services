# Client config for deb mirror

Use the following to fetch deb packages from your mirror-host by configuring `/etc/apt/sources.list` or similar:

```list
deb [trusted=yes arch=amd64,arm64 arch-=i386,armel,armhf] https://mirror.services.osism.tech/deb/ default  all
```

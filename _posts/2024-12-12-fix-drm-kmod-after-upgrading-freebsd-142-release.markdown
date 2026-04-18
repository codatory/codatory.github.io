---
layout: post
title:  "Fix drm-kmod after upgrading FreeBSD to 14.2-RELEASE"
date:   2024-12-12 00:00:00 -0500
categories: 
---

Caution: this is probably not the best way to do this. I took a break from FreeBSD and am just getting back into it.

Do this from your "broken" install of 14.2. You may need to use an alternate console or SSH.

### Prep Ports and OS Sources

```
pkg install -y git portmaster

git clone --branch releng/14.2 https://github.com/freebsd/freebsd-src.git /usr/src

git clone --branch main https://github.com/freebsd/freebsd-ports.git /usr/ports
```

### Rebuild drm-kmod and drm-kmod-61

```
pkg remove drm-kmod drm-61-kmod drm-515-kmod drm-510-kmod

portmaster -f --packages-build -r drm-kmod drm-61-kmod
```

### Reboot

Hope you work now!

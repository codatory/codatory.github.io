---
layout: post
title:  "Hello Keepalived"
date:   2022-12-03 9:00:00 -0400
categories: k8s
---

My K8S cluster has been pretty flaky, with lots of errors on the KubeAPI and Metrics Server going unavailable regularly. I was also frequently unable to get logs from my pods. Turns out I should've read the K0S documentation better.

> Control plane high availability requires a tcp load balancer, which acts as a single point of contact to access the controllers.

Well, the hardware I have is really the hardware I want to use in this cluster. Sure I could spin up some VMs or Raspberry Pis to do the load balancing but I'd much rather use the hardware that's there. We aren't pushing things super hard, so it shouldn't be super demanding or anything.

So, I pulled out my old pal Keepalived. My original plan was to use LVS to load balance the services, but after repeated problems with getting the port bindings to work reliably I decided load balancing wasn't really that necessary either. Instead, I'm going to allow keepalived to float around an IP and k0s will bind to it directly. This means if I _do_ get more API traffic than a single node can handle to the floating IP I'll have problems. I don't expect problems.

To make it work, you need to enable a Linux kernel feature called nonlocal bind. This allows services to bind to addresses that aren't physically present on the server. Then I have keepalived configured to monitor the K0S processes and float the IP address to the server with the most services working. Per usual, here's an [Ansible Playbook](https://gist.github.com/codatory/b6e59b3752cf97b56d8f0417ae9ce9fa) with my configuration. You'll probably need to sub in your interface IDs and the IP you want to use as a floater.

Once it's configured, you'll need to update your k0sctl config to have it use the new floating IP. You do this by setting the externalAddress on the API Server and populating the SANs with all valid addresses (and hostnames) for your cluster.

```yaml
  k0s:
    version: 1.25.4+k0s.0
    dynamicConfig: false
    config:
      spec:
        api:
          externalAddress: 10.8.0.10
          sans:
            - 10.8.0.10
            - 127.0.0.1
            - 10.8.0.11
            - 10.8.0.12
            - 10.8.0.13
```
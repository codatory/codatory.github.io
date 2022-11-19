---
layout: post
title:  "Hello Kubernetes"
date:   2022-11-18 19:00:00 -0400
categories: k8s
---

Staring down the end of life of my existing vSphere cluster
I decided I wanted to refresh on something a little lighter
weight and more modern. My need to run traditional VMs has
all but evaporated, with a number of my fleet being VMs that
existed simply to host a container or set of containers.

Having just completed some significant Kubernetes training,
I decided keeping myself fresh on the subject was another
benefit I should try and enjoy from a refresh. Therefore,
rather than rebuilding on a large node I decided to go for
a multi-node cluster of some small, lower power machines.

The new cluster is built on a number of Dell Optiplex Micro
form factor desktop machines, 3 dedicated to the control
plane and 3 dedicated to hosting application workloads.
Persistent storage is hosted on a QNAP NAS and made 
available over NFS.

This blog series will go into the actual software deployed
on the cluster, because that's actually more interesting
than the hardware. Any VM or hardware you've got around is
probably fine to run the software, depending on your
resource and redundancy requirements. For a redundant 
control plane, you need to have 3 nodes but you can run
everything on a single host if you're interested in it.
---
layout: post
title:  "Hello Host Patching"
date:   2022-11-20 9:00:00 -0400
categories: k8s
---

Well, it's been a few days and now we want to check for updates on our host systems and be able to patch them. After all, we can't deploy workloads until we have reached some baseline operational maturity. While there are some cluster-native ways to orchestrate patching I'm still happy to have my legacy tooling (Ansible) do it as a slightly simpler workflow.

Patching a K8S cluster isn't entirely difficult or entirely straightforward, there are a few things that need to happen in sequence to make sure everything goes off well. First off, you don't want to induce too much load on the cluster at once. Second off, becore you take a node offline you need to drain the pods off of it, and lastly when the node is ready you need to uncordon it to allow work to be scheduled on it again.

My [Ansible Playbook](https://gist.github.com/codatory/44e4944a1363e9ffadb9db2d0919b672) to do that is here. It uses needrestart to check for services that need restarted and if a reboot is required does all the dran/uncordon work using kubectl on the admin workstation.
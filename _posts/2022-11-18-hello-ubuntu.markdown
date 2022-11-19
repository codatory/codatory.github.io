---
layout: post
title:  "Hello Ubuntu"
date:   2022-11-18 20:00:00 -0400
categories: k8s
---

Well, first thing's first. If we're going to commission some hardware
it needs an operating system. I've standardized on Ubuntu 20.04 for
everything, so that's what I'm running here. These nodes were built
using the Server Live ISO installed offline to ensure a minimal install
and then connected to the network.

I manage my systems with Ansible, and you'll find the [playbook](https://gist.github.com/codatory/c0dc6d425a95d7268754f2af6dece0ab) I used to prepare these systems. This playbook does a few simple things like upgrade the kernel to the HWE rolling release kernel and ensuring my user is allowed to sudo without a password prompt. To run the command you need a working version of Ansible, to populate the inventory file with your host information and have pre-exchanged SSH Keys. Then you can run the playbook with `ansible-playbook -i hosts.yml os-setup.yml`. I also provided the playbook I used to update the BIOS/EFI on my systems, which if you also select similar systems may work for you.
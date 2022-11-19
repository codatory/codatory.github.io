---
layout: post
title:  "Hello MetalLB"
date:   2022-11-18 22:00:00 -0400
categories: k8s
---

Ok, we need an easy way to connect services running in our cluster to the external network. The method I chose is MetalLB, because it's a very simple and flexible way to expose services without relying on an external load balancer. MetalLB plays well with the CNI (Kube-Proxy) used by k0s, so we don't need to do anything special to prepare for the installation. I already have Helm installed on my administration system, so deploying MetalLB is really simple. First we need to add the repository to Helm.

`helm repo add metallb https://metallb.github.io/metallb`

Once the repository is added, we can issue a command to have helm install (or update) MetalLB for us.

`helm upgrade --install --create-namespace --namespace metallb-system metallb metallb/metallb`

Once the chart has been installed, all the necessary pods will be downloaded and started on the appropriate servers. Lastly, we need to give the system some IP addresses to assign to services. We do this with a [YAML file](https://gist.github.com/codatory/d3a647a68955d5fdcc1d07383ab78cee) that we apply with `kubectl apply -f`. Be sure to select addresses that are available on the network your servers are attached to!

Oh did it fail for you too? In both of my installs applying the YAML file failed with a webhook error until I re-started the controller pod. No idea why. `kubectl -n metallb-system get pod | grep control | awk '{print $1}' | xargs kubectl delete -n metallb-system pod `ought to do the job to get you going.

Now, let's deploy something so we can test and make sure this thing is working. We'll deploy something called in Ingress, which is basically a shared web server that allows us to route traffic into the cluster using HTTP. The details don't matter right now, so let's just get going.

One again we need to add a repository to Helm:

`helm repo add traefik https://traefik.github.io/charts`

Then we will deploy the chart.

`helm upgrade --install --create-namespace --namespace traefik-system traefik traefik/traefik`

This will go and deploy some stuff for us, and once it's done we can run `kubectl -n traefik-system get services` and in the External-IP column you should have an IP that was in the range in the YAML file you provided. If you try and load that IP you should get a 404 error. Congrats!
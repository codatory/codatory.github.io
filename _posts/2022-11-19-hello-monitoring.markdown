---
layout: post
title:  "Hello Monitoring"
date:   2022-11-19 10:00:00 -0400
categories: k8s
---

Perfect, we've got storage sorted out and now we can run real applications. Let's deploy monitoring to our cluster so we can see how it's performing and check that everything is working correctly. We'll be deploying the Prometheus Stack, as this is the most popular and best supported monitoring solution for Kubernetes. Any guesses how this starts?

`helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`

Yep; a new helm repo. This chart needs enough options we'll go ahead and provide them with a [YAML file](https://gist.github.com/codatory/d6d62a02369d7ccf725b6a72bc92eeca). We're turning alertmanager off for now but you're welcome to learn how to configure it if you want. In Grafana we're setting a default timezone, enabling persistent storage, and exposing the service as a LoadBalancer (so that MetalLB will assign it an IP address) and working around a bug. The Prometheus section also has a long block to have it request storage as part of the deployment.

`helm upgrade --install --wait --create-namespace --namespace monitoring prometheus-stack prometheus-community/kube-prometheus-stack --values=prometheus.yml`

Once the deployment is completed, you should be able to run `kubectl get svc -n monitoring` to find the IP address for Grafana. Punch that into your browser and log in with admin prom-operator, and browse through the Dashboards page.
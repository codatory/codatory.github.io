---
layout: page
title: Posts
---

{% assign years = site.posts | group_by_exp: 'post', "post.date | date: '%Y'" %}
{% for year in years %}
## {{ year.name }}

{% include post-list.html posts=year.items %}

{% endfor %}

---
title: Posts
---

{% for post in site.posts %}
- [{{ post.title }}]({{post.url}}) - {{post.date}}
{% endfor %}
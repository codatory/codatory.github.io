---
layout: default
---

<p class="intro">{{ site.description | escape }}</p>

## Recent posts

{% assign recent_posts = site.posts | slice: 0, 5 %}
{% include post-list.html posts=recent_posts %}

[Browse all posts]({{ '/posts.html' | relative_url }})

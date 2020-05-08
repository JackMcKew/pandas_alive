{% extends 'markdown.tpl' %}
{% block codecell %}
``` python
{{cell.source}}
```
{% endblock codecell %}
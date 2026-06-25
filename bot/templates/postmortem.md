# Postmortem: {{ incident_id }}

**Title:** {{ title }}
**Severity:** {{ severity }}
**Date:** {{ declared_at }}
**Duration:** {{ duration }}

## Summary

{{ summary }}

## Timeline

{% for event in timeline %}
- **{{ event.timestamp }}** — {{ event.event }} (by {{ event.actor }})
{% endfor %}

## Root Causes (5 Whys)

{% for cause in root_causes %}
- {{ cause }}
{% endfor %}

## Action Items

{% for item in action_items %}
- [ ] {{ item }}
{% endfor %}

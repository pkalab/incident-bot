# Incident Response Bot

A Slack-native bot that automates incident response — creates war rooms,
runs diagnostic playbooks, and generates postmortems.

## Commands

| Command | Description |
|---------|-------------|
| `/incident <title>` | Declare an incident |
| `/incident resolve` | Resolve active incident |
| `/status <state>` | Update incident status |
| `/playbook <name>` | Run a diagnostic check |
| `/postmortem` | Generate postmortem |

## Quick Start

1. **Create a Slack app** at api.slack.com with Socket Mode enabled
2. **Copy `.env.example` to `.env`** and fill in your SLACK_* tokens
3. **Run locally:**
   ```bash
   make install
   make run
   ```
4. **Deploy:**
   ```bash
   cd terraform && terraform apply
   ```

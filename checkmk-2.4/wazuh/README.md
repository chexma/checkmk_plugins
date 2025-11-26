# Wazuh CheckMK Plugin

A CheckMK 2.4 Special Agent plugin for monitoring [Wazuh](https://wazuh.com/) SIEM/XDR via its REST API.

## Features

- Monitor Wazuh Manager process status
- Cluster health and node synchronization status
- Agent statistics (active, disconnected, pending, never connected)
- Daemon statistics (analysisd, remoted, wazuh-db)
- Log monitoring (errors, warnings, critical)
- Ruleset status (rules and decoders count)
- Outdated agents detection
- Background tasks monitoring
- Individual agent monitoring via piggyback
- Security Configuration Assessment (SCA) per agent
- File Integrity Monitoring (Syscheck) status per agent
- Configurable thresholds for all checks
- Graphs and perfometers for all metrics

## Services

### Manager Services

| Service | Description |
|---------|-------------|
| **Wazuh API** | API connectivity, version info |
| **Wazuh Manager** | Manager process status (analysisd, remoted, syscheckd, etc.) |
| **Wazuh Cluster** | Cluster enabled/running, node count, sync status |
| **Wazuh Agents** | Summary: total, active, disconnected, pending agents |
| **Wazuh Daemon %s** | Per-daemon statistics (wazuh-remoted, wazuh-analysisd, wazuh-db) |
| **Wazuh Logs** | Log summary: errors, warnings, critical counts |
| **Wazuh Ruleset** | Rules and decoders count |
| **Wazuh Agents Outdated** | Number and list of outdated agents |
| **Wazuh Tasks** | Background task status (in progress, pending, done, failed) |

### Piggyback Services (per Agent)

| Service | Description |
|---------|-------------|
| **Wazuh Agent** | Individual agent status, version, OS, last keepalive |
| **Wazuh SCA %s** | Security Configuration Assessment per policy |
| **Wazuh Syscheck** | File Integrity Monitoring scan status |

## Requirements

- CheckMK 2.4+
- Wazuh Manager with API enabled (default port 55000)
- API user credentials with read permissions

## Installation

Install the MKP in your checkmk site.

## Configuration

1. **Create a rule** at: Setup � Agents � Other integrations � **Wazuh SIEM/XDR**

2. Configure the connection:
   - API Port (default: 55000)
   - Username (default: wazuh)
   - Password
   - SSL certificate verification (disable for self-signed certs)
   - Timeout
   - Piggyback options:
     - Create piggyback data for disconnected agents
     - Include active agents in piggyback
     - Collect SCA data for piggyback agents
     - Collect Syscheck data for piggyback agents

3. **Configure the host**:
   - Set "Monitoring agents" to "Configured API integrations, no Checkmk agent" or include both

4. Run service discovery:


## Testing

Test the special agent directly:
```bash
~/local/lib/python3/cmk_addons/plugins/wazuh/libexec/agent_wazuh \
    --hostname <WAZUH_MANAGER_IP> \
    --port 55000 \
    --username wazuh-wui \
    --password '<API_PASSWORD>' \
    --no-cert-check
```

**Note**: The Wazuh API runs on port 55000 by default (not 443, which is the dashboard).

Debug via CheckMK:
```bash
cmk --debug -d <hostname>
```

## Default Thresholds

### Wazuh Agents
| Metric | WARN | CRIT |
|--------|------|------|
| Disconnected agents | 1 | 5 |
| Disconnected % | 5% | 10% |
| Never connected | 5 | 10 |
| Pending | 10 | 20 |

### Wazuh Manager
Required processes (CRIT if stopped):
- wazuh-analysisd
- wazuh-remoted
- wazuh-syscheckd
- wazuh-logcollector
- wazuh-modulesd
- wazuh-db
- wazuh-execd

### Wazuh Daemon Stats
| Metric | WARN | CRIT |
|--------|------|------|
| Queue usage | 70% | 90% |

### Wazuh Logs
| Metric | WARN | CRIT |
|--------|------|------|
| Errors | 1 | 10 |
| Warnings | 10 | 50 |

### Wazuh Agents Outdated
| Metric | WARN | CRIT |
|--------|------|------|
| Outdated agents | 1 | 5 |

### Wazuh Tasks
| Metric | WARN | CRIT |
|--------|------|------|
| Failed tasks | 1 | 5 |

### Wazuh SCA (per agent)
| Metric | WARN | CRIT |
|--------|------|------|
| Score below | 70% | 50% |
| Failed checks | 10 | 25 |

### Wazuh Syscheck (per agent)
| Metric | WARN | CRIT |
|--------|------|------|
| Scan age | 1 day | 2 days |

## License

GPL 2.0

## Version

See [Changelog.md](Changelog.md)

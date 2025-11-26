# Wazuh CheckMK Plugin

A CheckMK 2.4 Special Agent plugin for monitoring [Wazuh](https://wazuh.com/) SIEM/XDR via its REST API.

## Features

- Monitor Wazuh Manager process status
- Cluster health and node synchronization status
- Agent statistics (active, disconnected, pending, never connected)
- Individual agent monitoring via piggyback
- Configurable thresholds for all checks
- Graphs and perfometers for agent metrics

## Services

| Service | Description |
|---------|-------------|
| **Wazuh API** | API connectivity, version info |
| **Wazuh Manager** | Manager process status (analysisd, remoted, syscheckd, etc.) |
| **Wazuh Cluster** | Cluster enabled/running, node count, sync status |
| **Wazuh Agents** | Summary: total, active, disconnected, pending agents |
| **Wazuh Agent** | Individual agent status (via piggyback) |

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
   - Piggyback options for individual agents

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

## License

GPL 2.0

## Version

See [Changelog.md](Changelog.md)

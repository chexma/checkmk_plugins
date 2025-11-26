# CHANGELOG

- **0.0.4** - 26.11.2025 - Bug fix
  - Fixed agent summary parsing: API returns `data.connection.*` not `data.affected_items[0].*`

- **0.0.2** - 26.11.2025 - Extended monitoring capabilities
  - New services: Daemon Stats, Logs, Ruleset, Outdated Agents, Tasks
  - New piggyback services: SCA (Security Configuration Assessment), Syscheck
  - Added 40+ new metrics with graphs and perfometers
  - Added configurable thresholds for all new checks
  - Updated special agent with 8 new API endpoints
  - Added piggyback options for SCA and Syscheck data collection

- **0.0.1** - 26.11.2025 - First Version of special agent
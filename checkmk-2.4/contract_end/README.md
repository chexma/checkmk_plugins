# CheckMK Contract End Date Monitoring Plugin

A CheckMK plugin for monitoring hardware support contracts by their expiration dates. This plugin alerts you when contracts are approaching their end date based on configurable thresholds.

## Features

- Monitor multiple contracts per host or globally
- Flexible date format support (ISO 8601, European, US formats)
- Configurable warning and critical thresholds
- Automatic metric generation for trending and graphing
- Additional information field for contract notes
- No agent plugin required (passive check)

## Installation

### 1. Install the Check Plugin

## Configuration

### 1. Create a Rule

1. In the CheckMK web interface, go to **Setup > Services > Service monitoring rules**
2. Search for "Contract End Date Monitoring"
3. Click on the rule to create a new entry
4. Configure the following parameters:

#### Required Parameters

- **Contract Name**: Name of the contract (used as service name)
  - Example: "Dell Server Support 2025"

- **Contract End Date**: The expiration date of the contract
  - Format depends on the selected date format
  - Example: "2025-12-31"

- **Date Format**: Select the format of your end date
  - ISO 8601 (YYYY-MM-DD)
  - ISO 8601 with time (YYYY-MM-DD HH:MM:SS)
  - European format (DD.MM.YYYY)
  - European format with slash (DD/MM/YYYY)
  - US format (MM/DD/YYYY)
  - US format with dash (MM-DD-YYYY)

- **Time Remaining Thresholds**:
  - **Warning at**: Time remaining when state becomes WARNING
    - Default: 30 days
    - Example: Set to 60 days for long-term contracts
  - **Critical at**: Time remaining when state becomes CRITICAL
    - Default: 7 days
    - Example: Set to 14 days for critical contracts

#### Optional Parameters

- **Additional Information**: Free-text field for contract notes
  - Contract number
  - Vendor contact information
  - Renewal procedures
  - Any other relevant information

### 2. Assign the Rule to Hosts

You can assign the rule to:
- Specific hosts
- Host groups
- Folders
- All hosts (global monitoring)

### 3. Discovery

After creating the rule:

1. Go to the host(s) where the rule applies
2. Run **Service Discovery**
3. You should see a new service: "Contract: [Your Contract Name]"
4. Accept the changes

## File Locations

**CheckMK Site Structure (CheckMK 2.0+):**
```
/omd/sites/<SITENAME>/
├── local/
│   └── lib/python3/cmk_addons/plugins/contracts/
│       ├── agent_based/
│       │   └── contract_enddate.py              # Check plugin
│       └── rulesets/
│           └── ruleset_contract_enddate.py      # Ruleset parameters
```

## Development

This plugin uses CheckMK Plugin API v2.

**Key Components:**
- `discover_contract_enddate()`: Creates services based on ruleset
- `check_contract_enddate()`: Performs the actual check and comparison
- `parse_date()`: Handles multiple date format parsing
- `format_time_remaining()`: Formats output in human-readable format

## License

GPLv3

## Support

## Version History

- **v1.0** (2025): Initial release
  - Basic contract monitoring
  - Multiple date format support
  - Configurable thresholds
  - Metric generation

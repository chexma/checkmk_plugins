<#
.SYNOPSIS
    Sets a host downtime in CheckMK using the REST API.

.DESCRIPTION
    This script connects to the CheckMK REST API and sets a downtime for the local host.
    It can run in automatic mode (using configuration values) or interactive mode
    (prompting for comment and duration).

.PARAMETER Interactive
    Enables interactive mode where the user is prompted for comment and duration.

.PARAMETER Duration
    Override the default downtime duration in seconds.

.PARAMETER Comment
    Override the default downtime comment.

.PARAMETER Hostname
    Override the local hostname. If not specified, uses the local computer name.

.EXAMPLE
    .\checkmk-rest-downtime.ps1
    Sets a downtime using configuration values.

.EXAMPLE
    .\checkmk-rest-downtime.ps1 -Interactive
    Prompts for comment and duration before setting the downtime.

.EXAMPLE
    .\checkmk-rest-downtime.ps1 -Duration 600 -Comment "Server maintenance"
    Sets a 10-minute downtime with custom comment.

.EXAMPLE
    .\checkmk-rest-downtime.ps1 -Hostname "server01" -Duration 300
    Sets a 5-minute downtime for a specific host.

.NOTES
    Author: Andre.Eckstein@Bechtle.com
    Requires: PowerShell 5.1 or later
    The automation user needs the permission: action.downtimes
#>

param(
    [Parameter(Mandatory = $false)]
    [switch]$Interactive,

    [Parameter(Mandatory = $false)]
    [int]$Duration,

    [Parameter(Mandatory = $false)]
    [string]$Comment,

    [Parameter(Mandatory = $false)]
    [string]$Hostname
)

#####################################################
# Set a Host Downtime in CheckMK using the REST API #
# Andre.Eckstein@Bechtle.com                        #
#####################################################

#################
# Configuration #
#################

# Resolvable Hostname or IP Address of the CheckMK server (include port if needed)
# Note: Use 127.0.0.1 instead of "localhost" if you experience IPv6/IPv4 issues
$CheckmkServer = "127.0.0.1:5000"

# CheckMK site name
$CheckmkSite = "cmk"

# Protocol http or https
$protocol = "http"

# CheckMK automation user who sets the downtime
$DowntimeUser = "cmkadmin"

# CheckMK automation secret of the above user (not the login password!)
$AutomationSecret = "cmkadmin"

# Default duration of the CheckMK Downtime in seconds
$DefaultDowntimeDuration = 300

# Default comment for the downtime (username will be automatically prefixed)
$DefaultDowntimeComment = "Host downtime set by PowerShell script."

# Convert local Windows hostname to exactly match the hostname in CheckMK
# Possible options: disabled | lowercase | uppercase | titlecase
$ConvertHostname = "lowercase"

# Add domain name to the hostname to exactly match the hostname in CheckMK
# Possible options: "" for no domain suffix or ".mydomain.tld" for FQDN
$DomainSuffix = ""

# Enable Debug Output: $true | $false
$Debug = $false

# Ignore SSL/TLS errors with self-signed certificates: $true | $false
$IgnoreTlsErrors = $true


########
# Code #
########

#############
# Functions #
#############

function Get-TransformedHostname {
    param(
        [Parameter(Mandatory)]
        [string]$Hostname,
        [string]$ConvertMode,
        [string]$DomainSuffix
    )

    # Apply case conversion
    switch ($ConvertMode) {
        "lowercase" { $Hostname = $Hostname.ToLower() }
        "uppercase" { $Hostname = $Hostname.ToUpper() }
        "titlecase" { $Hostname = $Hostname.Substring(0,1).ToUpper() + $Hostname.Substring(1).ToLower() }
        "disabled"  { } # Keep as-is
        default     { Write-Warning "Unknown conversion mode: $ConvertMode" }
    }

    # Add domain suffix if specified
    if ($DomainSuffix) {
        $DomainSuffix = $DomainSuffix.TrimStart(".")
        $Hostname = "$Hostname.$DomainSuffix"
    }

    return $Hostname
}


########
# Main #
########

# Get current username for comment prefix
$CurrentUser = [Environment]::UserName

# Determine downtime duration
if ($Duration -gt 0) {
    $DowntimeDuration = $Duration
}
elseif ($Interactive) {
    $inputDuration = Read-Host "Enter downtime duration in seconds (default: $DefaultDowntimeDuration)"
    if ($inputDuration -match '^\d+$' -and [int]$inputDuration -gt 0) {
        $DowntimeDuration = [int]$inputDuration
    }
    else {
        $DowntimeDuration = $DefaultDowntimeDuration
        Write-Host "Using default duration: $DowntimeDuration seconds" -ForegroundColor Yellow
    }
}
else {
    $DowntimeDuration = $DefaultDowntimeDuration
}

# Determine downtime comment
if ($Comment) {
    $DowntimeComment = "${CurrentUser}: $Comment"
}
elseif ($Interactive) {
    $inputComment = Read-Host "Enter downtime comment (default: $DefaultDowntimeComment)"
    if ($inputComment) {
        $DowntimeComment = "${CurrentUser}: $inputComment"
    }
    else {
        $DowntimeComment = "${CurrentUser}: $DefaultDowntimeComment"
    }
}
else {
    $DowntimeComment = "${CurrentUser}: $DefaultDowntimeComment"
}

# Get and transform hostname
if ($Hostname) {
    # Use provided hostname (no transformation)
    $TargetHostname = $Hostname
}
else {
    # Use local computer name with transformation
    $TargetHostname = Get-TransformedHostname -Hostname $env:COMPUTERNAME -ConvertMode $ConvertHostname -DomainSuffix $DomainSuffix
}

if ($Debug) {
    Write-Host "Hostname: $TargetHostname" -ForegroundColor Cyan
    Write-Host "Comment: $DowntimeComment" -ForegroundColor Cyan
}

# Ignore TLS errors if configured
if ($IgnoreTlsErrors) {
    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
}

# Calculate downtime times (UTC for API, local for display)
$now_local = Get-Date
$now_utc = $now_local.ToUniversalTime()
$StartTimeUTC = $now_utc.ToString("yyyy-MM-ddTHH:mm:ssZ")
$EndTimeUTC = $now_utc.AddSeconds($DowntimeDuration).ToString("yyyy-MM-ddTHH:mm:ssZ")
$StartTimeLocal = $now_local.ToString("yyyy-MM-dd HH:mm:ss")
$EndTimeLocal = $now_local.AddSeconds($DowntimeDuration).ToString("yyyy-MM-dd HH:mm:ss")

if ($Debug) {
    Write-Host "Duration: $DowntimeDuration seconds" -ForegroundColor Cyan
    Write-Host "Start: $StartTimeLocal" -ForegroundColor Cyan
    Write-Host "End: $EndTimeLocal" -ForegroundColor Cyan
}

# Build request
$Uri = "{0}://{1}/{2}/check_mk/api/1.0/domain-types/downtime/collections/host" -f $protocol, $CheckmkServer, $CheckmkSite

$Headers = @{
    'Content-Type'  = 'application/json'
    'Authorization' = "Bearer $DowntimeUser $AutomationSecret"
    'Accept'        = 'application/json'
}

$Body = @{
    start_time    = $StartTimeUTC
    end_time      = $EndTimeUTC
    comment       = $DowntimeComment
    host_name     = $TargetHostname
    downtime_type = 'host'
} | ConvertTo-Json -Compress

if ($Debug) {
    Write-Host "URI: $Uri" -ForegroundColor Cyan
    Write-Host "Body: $Body" -ForegroundColor Cyan
}

# Send request
try {
    $Response = Invoke-WebRequest -Method Post -Uri $Uri -Headers $Headers -Body $Body -ContentType "application/json"

    Write-Host ""
    Write-Host "SUCCESS: Downtime set for host '$TargetHostname'" -ForegroundColor Green
    Write-Host "  From: $StartTimeLocal" -ForegroundColor Green
    Write-Host "  Until: $EndTimeLocal" -ForegroundColor Green
    Write-Host "  Duration: $DowntimeDuration seconds" -ForegroundColor Green
    Write-Host "  Comment: $DowntimeComment" -ForegroundColor Green
    exit 0
}
catch {
    $StatusCode = [int]$_.Exception.Response.StatusCode
    $ErrorMessage = $_.Exception.Message

    Write-Host ""
    Write-Host "ERROR: Failed to set downtime for host '$TargetHostname'" -ForegroundColor Red
    Write-Host "  Server: $CheckmkServer" -ForegroundColor Red
    Write-Host "  HTTP Status: $StatusCode" -ForegroundColor Red
    Write-Host "  Message: $ErrorMessage" -ForegroundColor Red

    # Try to get response body for more details
    try {
        $ResponseBody = $_.ErrorDetails.Message
        if ($ResponseBody) {
            $ErrorDetails = $ResponseBody | ConvertFrom-Json
            if ($ErrorDetails.detail) {
                Write-Host "  Detail: $($ErrorDetails.detail)" -ForegroundColor Red
            }
        }
    }
    catch {
        # Ignore JSON parsing errors
    }

    exit 1
}

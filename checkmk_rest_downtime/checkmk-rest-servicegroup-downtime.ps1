<#
.SYNOPSIS
    Sets a downtime for all services in a CheckMK servicegroup using the REST API.

.DESCRIPTION
    This script connects to the CheckMK REST API and sets a downtime for all services
    that belong to a specified servicegroup.

.PARAMETER ServiceGroup
    The name of the servicegroup in CheckMK. Overrides the $ServiceGroupName configuration variable.

.PARAMETER Secret
    The automation secret as SecureString. If not provided and $AutomationSecret is empty,
    you will be prompted to enter it interactively.

.EXAMPLE
    .\checkmk-rest-servicegroup-downtime.ps1
    Sets a downtime using the default servicegroup from the configuration.

.EXAMPLE
    .\checkmk-rest-servicegroup-downtime.ps1 -ServiceGroup "backup_services"
    Sets a downtime for all services in the servicegroup "backup_services".

.EXAMPLE
    $secret = Read-Host -AsSecureString
    .\checkmk-rest-servicegroup-downtime.ps1 -Secret $secret
    Sets a downtime using a pre-defined SecureString secret.

.NOTES
    Author: Andre.Eckstein@Bechtle.com
    Requires: PowerShell 5.1 or later
    The automation user needs the permission: action.downtimes
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$ServiceGroup,

    [Parameter(Mandatory = $false)]
    [SecureString]$Secret
)

#############################################################
# Set a Servicegroup Downtime in CheckMK using the REST API #
# Andre.Eckstein@Bechtle.com                                #
#############################################################

#################
# Configuration #
#################

# Resolvable Hostname or IP Address of the CheckMK server (include port if needed)
# Note: Use 127.0.0.1 instead of "localhost" if you experience IPv6/IPv4 issues
$CheckmkServer = ""

# CheckMK site name
$CheckmkSite = ""

# Protocol http or https
$protocol = ""

# CheckMK automation user who sets the downtime
$DowntimeUser = ""

# CheckMK automation secret of the above user (not the login password!)
# Leave empty to use interactive prompt or -Secret parameter
$AutomationSecret = ""

# Duration of the CheckMK Downtime in seconds
$DowntimeDuration = 300

# Comment for the downtime (username will be automatically prefixed)
$DowntimeComment = "Servicegroup downtime set by PowerShell script."

# Prefix comment with current username
$CurrentUser = [Environment]::UserName
$DowntimeComment = "${CurrentUser}: ${DowntimeComment}"

# Default servicegroup name (can be overridden by -ServiceGroup parameter)
$ServiceGroupName = ""

# Enable Debug Output: $true | $false
$Debug = $true

# Ignore SSL/TLS errors with self-signed certificates: $true | $false
$IgnoreTlsErrors = $true


########
# Main #
########

# Determine automation secret (priority: parameter > config > prompt)
if ($Secret) {
    # Convert SecureString from parameter to plain text
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Secret)
    $AutomationSecret = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)
}
elseif (-not $AutomationSecret) {
    # Prompt for secret if not configured
    Write-Host "Enter automation secret for user '$DowntimeUser':" -ForegroundColor Yellow
    $SecureSecret = Read-Host -AsSecureString
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureSecret)
    $AutomationSecret = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)
}

# Determine target servicegroup
if ($ServiceGroup) {
    $TargetServiceGroup = $ServiceGroup
}
elseif ($ServiceGroupName) {
    $TargetServiceGroup = $ServiceGroupName
}
else {
    Write-Host "ERROR: No servicegroup specified. Use -ServiceGroup parameter or set `$ServiceGroupName in configuration." -ForegroundColor Red
    exit 1
}

if ($Debug) {
    Write-Host "Servicegroup: $TargetServiceGroup" -ForegroundColor Cyan
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
$Uri = "{0}://{1}/{2}/check_mk/api/1.0/domain-types/downtime/collections/service" -f $protocol, $CheckmkServer, $CheckmkSite

$Headers = @{
    'Content-Type'  = 'application/json'
    'Authorization' = "Bearer $DowntimeUser $AutomationSecret"
    'Accept'        = 'application/json'
}

$Body = @{
    start_time        = $StartTimeUTC
    end_time          = $EndTimeUTC
    comment           = $DowntimeComment
    servicegroup_name = $TargetServiceGroup
    downtime_type     = 'servicegroup'
} | ConvertTo-Json -Compress

if ($Debug) {
    Write-Host "URI: $Uri" -ForegroundColor Cyan
    Write-Host "Body: $Body" -ForegroundColor Cyan
}

# Send request
try {
    $Response = Invoke-WebRequest -Method Post -Uri $Uri -Headers $Headers -Body $Body -ContentType "application/json"

    Write-Host ""
    Write-Host "SUCCESS: Downtime set for servicegroup '$TargetServiceGroup'" -ForegroundColor Green
    Write-Host "  From: $StartTimeLocal" -ForegroundColor Green
    Write-Host "  Until: $EndTimeLocal" -ForegroundColor Green
    Write-Host "  Duration: $DowntimeDuration seconds" -ForegroundColor Green
    exit 0
}
catch {
    $StatusCode = [int]$_.Exception.Response.StatusCode
    $ErrorMessage = $_.Exception.Message

    Write-Host ""
    Write-Host "ERROR: Failed to set downtime for servicegroup '$TargetServiceGroup'" -ForegroundColor Red
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
            if ($ErrorDetails.title) {
                Write-Host "  Title: $($ErrorDetails.title)" -ForegroundColor Red
            }
        }
    }
    catch {
        # Ignore JSON parsing errors
    }

    exit 1
}

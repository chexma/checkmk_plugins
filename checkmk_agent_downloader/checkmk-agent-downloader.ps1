<#
.SYNOPSIS
    Downloads CheckMK agents for multiple hosts via the REST API.

.DESCRIPTION
    This script connects to the CheckMK REST API and downloads agent packages
    for a list of hosts. It creates a CSV log file with download results
    including hostname, filename, agent hash, and SHA256 file hash.

.PARAMETER Hosts
    Comma-separated list of hostnames (e.g., "host1,host2,host3").

.PARAMETER HostFile
    Path to a text file containing hostnames (one per line).

.PARAMETER OsType
    The operating system type for the agent package.
    Valid values: windows_msi, linux_deb, linux_rpm, linux_tgz, aix_tgz, solaris_pkg, solaris_tgz
    Default: windows_msi

.PARAMETER OutputPath
    Directory where downloaded agents will be saved. Default: current directory.

.PARAMETER LogFile
    Path to the CSV log file. Default: download_log.csv in OutputPath.

.EXAMPLE
    .\checkmk-agent-downloader.ps1 -Hosts "server01,server02,server03"
    Downloads Windows MSI agents for the specified hosts.

.EXAMPLE
    .\checkmk-agent-downloader.ps1 -HostFile "hosts.txt" -OsType "linux_deb" -OutputPath "C:\Downloads"
    Downloads Linux DEB agents for hosts listed in hosts.txt.

.EXAMPLE
    .\checkmk-agent-downloader.ps1 -Hosts "webserver01" -OsType "linux_rpm" -LogFile "C:\Logs\agents.csv"
    Downloads a Linux RPM agent with custom log file location.

.NOTES
    Author: Andre.Eckstein@Bechtle.com
    Requires: PowerShell 5.1 or later
    The automation user needs permissions: wato.download_agents or wato.download_all_agents
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$Hosts,

    [Parameter(Mandatory = $false)]
    [string]$HostFile,

    [Parameter(Mandatory = $false)]
    [ValidateSet("windows_msi", "linux_deb", "linux_rpm", "linux_tgz", "aix_tgz", "solaris_pkg", "solaris_tgz")]
    [string]$OsType = "windows_msi",

    [Parameter(Mandatory = $false)]
    [string]$OutputPath = ".",

    [Parameter(Mandatory = $false)]
    [string]$LogFile
)

###########################################################
# Download CheckMK Agents for multiple hosts via REST API #
# Andre.Eckstein@Bechtle.com                              #
###########################################################

#################
# Configuration #
#################

# CheckMK Server (include port if needed)
# Note: Use 127.0.0.1 instead of "localhost" if you experience IPv6/IPv4 issues
$CheckmkServer = ""

# CheckMK site name
$CheckmkSite = ""

# Protocol http or https
$Protocol = "https"

# CheckMK automation user
$Username = ""

# CheckMK automation secret (not the login password!)
$AutomationSecret = ""

# Ignore SSL/TLS errors with self-signed certificates: $true | $false
$IgnoreSSL = $true

# Enable debug output: $true | $false
$Debug = $false


########
# Code #
########

#############
# Functions #
#############

function Download-AgentForHost {
    param(
        [Parameter(Mandatory)]
        [string]$HostName,
        [Parameter(Mandatory)]
        [string]$OsType,
        [Parameter(Mandatory)]
        [string]$OutputPath
    )

    $ApiUrl = "{0}://{1}/{2}/check_mk/api/1.0/domain-types/agent/actions/download_by_host/invoke" -f $Protocol, $CheckmkServer, $CheckmkSite
    $ApiUrl += "?os_type=$OsType&host_name=$HostName&agent_type=host_name"

    $Headers = @{
        "Authorization" = "Bearer $Username $AutomationSecret"
        "Accept"        = "application/octet-stream"
    }

    $Result = @{
        Hostname    = $HostName
        Filename    = ""
        AgentHash   = ""
        SHA256      = ""
        Status      = "Failed"
        Error       = ""
        Timestamp   = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    }

    try {
        # Create temporary file for download
        $TempFile = [System.IO.Path]::GetTempFileName()

        $InvokeParams = @{
            Uri         = $ApiUrl
            Method      = 'GET'
            Headers     = $Headers
            OutFile     = $TempFile
            ErrorAction = 'Stop'
            PassThru    = $true
        }

        # Handle SSL certificate validation
        if ($PSVersionTable.PSVersion.Major -ge 7 -and $IgnoreSSL) {
            $InvokeParams['SkipCertificateCheck'] = $true
        }
        elseif ($IgnoreSSL) {
            [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
        }

        if ($Debug) {
            Write-Host "Debug: Downloading agent for $HostName..." -ForegroundColor Cyan
            Write-Host "Debug: URL: $ApiUrl" -ForegroundColor Cyan
        }

        # Download the agent
        $Response = Invoke-WebRequest @InvokeParams

        # Extract filename from Content-Disposition header
        $ContentDisposition = $Response.Headers['Content-Disposition']
        if ($ContentDisposition) {
            # Handle both array and string formats
            $DispositionValue = if ($ContentDisposition -is [array]) { $ContentDisposition[0] } else { $ContentDisposition }
            if ($DispositionValue -match 'filename[^;=\n]*=\s*"?([^";\n]+)"?') {
                $OriginalFilename = $Matches[1].Trim('"')
            }
            else {
                $OriginalFilename = "agent_${HostName}.${OsType}"
            }
        }
        else {
            $OriginalFilename = "agent_${HostName}.${OsType}"
        }

        # Extract agent hash from filename (format: check_mk_agent-<hash>.<ext>)
        if ($OriginalFilename -match '([a-fA-F0-9]{16})') {
            $Result.AgentHash = $Matches[1]
        }

        # Create final filename with hostname prefix
        $Extension = [System.IO.Path]::GetExtension($OriginalFilename)
        $FinalFilename = "${HostName}_${OriginalFilename}"
        $FinalPath = Join-Path -Path $OutputPath -ChildPath $FinalFilename

        # Move temp file to final location
        Move-Item -Path $TempFile -Destination $FinalPath -Force

        # Calculate SHA256 hash of downloaded file
        $FileHash = Get-FileHash -Path $FinalPath -Algorithm SHA256
        $Result.SHA256 = $FileHash.Hash

        $Result.Filename = $FinalFilename
        $Result.Status = "Success"

        if ($Debug) {
            Write-Host "Debug: Downloaded to $FinalPath" -ForegroundColor Cyan
            Write-Host "Debug: Agent Hash: $($Result.AgentHash)" -ForegroundColor Cyan
            Write-Host "Debug: SHA256: $($Result.SHA256)" -ForegroundColor Cyan
        }
    }
    catch {
        $Result.Error = $_.Exception.Message

        # Try to get more details from response
        try {
            if ($_.ErrorDetails.Message) {
                $ErrorDetails = $_.ErrorDetails.Message | ConvertFrom-Json
                if ($ErrorDetails.detail) {
                    $Result.Error = $ErrorDetails.detail
                }
            }
        }
        catch {
            # Keep original error message
        }

        # Clean up temp file if it exists
        if ($TempFile -and (Test-Path $TempFile)) {
            Remove-Item -Path $TempFile -Force -ErrorAction SilentlyContinue
        }
    }

    return $Result
}


########
# Main #
########

# Validate configuration
if (-not $CheckmkServer -or -not $CheckmkSite -or -not $Username -or -not $AutomationSecret) {
    Write-Host "ERROR: Please configure CheckmkServer, CheckmkSite, Username, and AutomationSecret in the script." -ForegroundColor Red
    exit 1
}

# Validate input parameters
if (-not $Hosts -and -not $HostFile) {
    Write-Host "ERROR: Please specify either -Hosts or -HostFile parameter." -ForegroundColor Red
    Write-Host "Example: .\checkmk-agent-downloader.ps1 -Hosts 'host1,host2,host3'" -ForegroundColor Yellow
    Write-Host "Example: .\checkmk-agent-downloader.ps1 -HostFile 'hosts.txt'" -ForegroundColor Yellow
    exit 1
}

# Build host list
$HostList = @()

if ($Hosts) {
    $HostList += $Hosts -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
}

if ($HostFile) {
    if (-not (Test-Path $HostFile)) {
        Write-Host "ERROR: Host file not found: $HostFile" -ForegroundColor Red
        exit 1
    }
    $HostList += Get-Content -Path $HostFile | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" -and $_ -notmatch '^\s*#' }
}

# Remove duplicates
$HostList = $HostList | Select-Object -Unique

if ($HostList.Count -eq 0) {
    Write-Host "ERROR: No hosts specified." -ForegroundColor Red
    exit 1
}

# Ensure output directory exists
if (-not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
}
$OutputPath = Resolve-Path $OutputPath

# Set default log file if not specified
if (-not $LogFile) {
    $LogFile = Join-Path -Path $OutputPath -ChildPath "download_log.csv"
}

# Initialize results
$Results = @()
$SuccessCount = 0
$FailedCount = 0

Write-Host ""
Write-Host "CheckMK Agent Bulk Downloader" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "Server: $CheckmkServer" -ForegroundColor Cyan
Write-Host "Site: $CheckmkSite" -ForegroundColor Cyan
Write-Host "OS Type: $OsType" -ForegroundColor Cyan
Write-Host "Hosts: $($HostList.Count)" -ForegroundColor Cyan
Write-Host "Output: $OutputPath" -ForegroundColor Cyan
Write-Host ""

# Process each host
$Counter = 0
foreach ($Host in $HostList) {
    $Counter++
    $ProgressPercent = [math]::Round(($Counter / $HostList.Count) * 100)

    Write-Progress -Activity "Downloading agents" -Status "Processing $Host ($Counter of $($HostList.Count))" -PercentComplete $ProgressPercent

    Write-Host "[$Counter/$($HostList.Count)] Downloading agent for: $Host" -NoNewline

    $Result = Download-AgentForHost -HostName $Host -OsType $OsType -OutputPath $OutputPath
    $Results += $Result

    if ($Result.Status -eq "Success") {
        $SuccessCount++
        Write-Host " [OK]" -ForegroundColor Green
    }
    else {
        $FailedCount++
        Write-Host " [FAILED]" -ForegroundColor Red
        Write-Host "   Error: $($Result.Error)" -ForegroundColor Red
    }
}

Write-Progress -Activity "Downloading agents" -Completed

# Export results to CSV
$Results | Export-Csv -Path $LogFile -NoTypeInformation -Encoding UTF8

# Summary
Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "Download Summary" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "Total: $($HostList.Count)" -ForegroundColor Cyan
Write-Host "Success: $SuccessCount" -ForegroundColor Green
Write-Host "Failed: $FailedCount" -ForegroundColor $(if ($FailedCount -gt 0) { "Red" } else { "Green" })
Write-Host ""
Write-Host "Log file: $LogFile" -ForegroundColor Cyan
Write-Host "Output directory: $OutputPath" -ForegroundColor Cyan

# Exit with error code if any downloads failed
if ($FailedCount -gt 0) {
    exit 1
}
exit 0

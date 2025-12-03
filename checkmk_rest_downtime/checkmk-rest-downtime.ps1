#####################################################
# Set a Host Downtime in checkmk using the REST API #
# Andre.Eckstein@Bechtle.com                        #
#####################################################

#################
# Configuration #
#################

# Resolvable Hostname or IP Adress of the checkmk server
$CheckmkServer = "192.168.215.11"

# checkmk site name
$CheckmkSite = "monitoring"

# protocol http or https <- (please :-)
$protocol = "http"

# checkmk automation user who sets the downtime
$DowntimeUser = "downtime_user"

# checkmk automation secret of the above user
$AutomationUserPassword = "12345678910"

# Duration of the checkmk Downtime
$DowntimeDuration = 300 # In seconds

# Comment that will be used for the checkmk downtime comment and in the Windows Event Log
$DowntimeComment = "Set by Powershell Downtime script."

# Type of Downtime
# Possible options: fixed | flexible
$DownTimeType = "fixed"

# Enable Debug Output, 
# Possible options: $true | $false
$Debug = $true

# Ignore SSL/TLS errors with self signed certificates
# Possible options: $true | $false
$IgnoreTlsErrors = $true

# Convert local Windows hostname to exactly match the hostname in checkmk 
# Possible options: disabled | lowercase | uppercase | titlecase
$ConvertHostname = "lowercase"

# Add domain name to the hostname to exactly match the hostname in checkmk
# Possible options: "" for no domain suffix or add your ".mydomain.whatever" for FQDN
$DomainSuffix = ""

# Logs Messages to the Windows "System" Log. Needs administrative rights one time to create the Event Source
# Possible options: $true | $false
$LogToEventLog = $true


########
# Code #
########

#############
# Functions #
#############

function AddDomainSuffix {
    [CmdletBinding()]
	param(
		[Parameter(Mandatory)]
		[string]$hostname,
        [string]$DomainSuffix
	)

    if ($Domainsuffix.StartsWith(".")) {
        $DomainSuffix = $Domainsuffix.Remove(0,1)
    }

    if ( $debug ) {
        write-host "Debug: Domain Suffix - Adding domain suffix ""$DomainSuffix"" to hostname ""$hostname"" "
    }

    $fqdn = "$hostname.$DomainSuffix"
    return $fqdn
}

function HostnametoUpperCase {
    [CmdletBinding()]
	param(
		[Parameter(Mandatory)]
		[string]$hostname
	)
    $hostname = $hostname.ToUpper()
    return $hostname
}

function HostnametoLowerCase {
    [CmdletBinding()]
	param(
		[Parameter(Mandatory)]
		[string]$hostname
	)
    $hostname = $hostname.ToLower()
    return $hostname
}

function HostnametoTitleCase {
    [CmdletBinding()]
	param(
		[Parameter(Mandatory)]
		[string]$hostname
	)
    $hostname = $hostname.substring(0,1).toupper()+$hostname.substring(1).tolower()
    return $hostname
}

function GetHostName {
        $hostname = ($env:COMPUTERNAME)
        return $hostname
    }

function RewriteHostname {
    [CmdletBinding()]
	param(
		[Parameter(Mandatory)]
		[string]$hostname,
        [string]$ConvertHostname
	)

    if ( $debug ) {
            write-host "Debug: Hostname conversion - Starting case conversion, conversion mode: $ConvertHostname"
        }

    if ( $ConvertHostname -eq "lowercase") {
        $hostname = HostnametoLowerCase $hostname
    }
    elseif ( $ConvertHostname -eq "uppercase") {
        $hostname = HostnametoUpperCase $hostname
    }
    elseif ( $ConvertHostname -eq "titlecase") {
        $hostname = HostnametoTitleCase $hostname
    }
    else {
        Write-Error "Conversion Case $ConvertHostname does not exist, please add correct option..."
    }

    return $hostname
}

function Test-Administrator  
{  
    [OutputType([bool])]
    param()
    process {
        [Security.Principal.WindowsPrincipal]$user = [Security.Principal.WindowsIdentity]::GetCurrent();
        return $user.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator);
    }
}

########
# Main #
########

$hostname = GetHostName

if ( $debug ) {
    write-host "Debug: Hostname : $hostname"
}

if ( $DomainSuffix ) {

    if ( $debug ) {
        write-host "Debug: Domain Suffix - Adding domain suffix enabled"
    }

    $hostname = AddDomainSuffix $hostname $DomainSuffix

    if ( $debug ) {
        write-host "Debug: Domain Suffix - Hostname after adding domain suffix : $hostname"
    }
}
else {
    if ( $debug ) {write-host "Debug: Domain Suffix - Not adding a domain suffix, none entered."}
}

if ($ConvertHostname -ne "disabled") {
    $hostname = RewriteHostname $hostname $ConvertHostname
}
else {
    if ( $Debug ) {
        write-host "Debug: Hostname conversion - Not doing any case conversion, intentionally disabled"
    }
}

if ( $debug ) { 
        write-host "Debug: Hostname conversion - Final Hostname after all conversions : $hostname" 
}

if ($IgnoreTlsErrors) {
    # Disable SSL verification
    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
}

# Get current time in UTC (CheckMK API expects UTC)
$now_utc = (Get-Date).ToUniversalTime()
$now_string = $now_utc.ToString("yyyy-MM-ddTHH:mm:ssZ")
$DowntimeEnds = $now_utc.AddSeconds($DowntimeDuration).ToString("yyyy-MM-ddTHH:mm:ssZ")

if ( $Debug ) {
    write-host "Debug: Downtime Duration: $DowntimeDuration seconds"
    write-host "Debug: Start time (UTC): $now_string"
    write-host "Debug: End time (UTC): $DowntimeEnds"
}

# Construct http Header
$Header = @{
    'Content-Type' = 'application/json'
    "authorization" = "Bearer $DowntimeUser $AutomationUserPassword"
    'Accept' = 'application/json'
} 

$Uri = "{0}://{1}/{2}/check_mk/api/1.0/domain-types/downtime/collections/host" -f $protocol, $CheckmkServer, $CheckmkSite

if ( $Debug ) {
    write-host "Debug: Constructed URI: $Uri"
}

$Body =@{  
    start_time = $now_string;
    end_time =   $DowntimeEnds;
    comment =  $DowntimeComment;
    host_name = $hostname;
    downtime_type = 'host';
    }  | ConvertTo-Json -Compress

$Parameters = @{
Method = "Post"
Uri = $Uri
Header = $Header
Body = $Body
ContentType = "application/json"
}

if ( $Debug ) {
    write-host "Debug: Parameters..."
    write-host $Parameters
}

$EventLogSource = "checkmk-downtime-script"
$DowntimeSuccess = $false

try {
    $result = Invoke-WebRequest @Parameters
    $DowntimeSuccess = $true

    $ResponseText = "StatusCode: {0}, Status: {1}" -f $result.StatusCode, $result.StatusDescription
    $LogMessage = "Successfully set a downtime from $now_string until $DowntimeEnds ($DowntimeDuration seconds). $ResponseText"

    if ( $Debug ) {
        write-host "Success: $LogMessage"
    }

} catch {
    $ResponseStatusCode = $_.Exception.Response.StatusCode
    $ResponseErrorMessage = $_.Exception.Message
    $ErrorText = "Unable to set downtime for host '$hostname' on checkmk server $CheckmkServer. "
    $ResponseErrorText = "StatusCode: {0}, Error: {1}" -f [int]$ResponseStatusCode, $ResponseErrorMessage
    $LogMessage = $ErrorText + $ResponseErrorText
    Write-Error -Message $LogMessage
}

# Write to Windows Event Log if enabled
if ( $LogToEventLog ) {
    $EventType = if ($DowntimeSuccess) { "Information" } else { "Error" }

    try {
        Write-EventLog -LogName "System" -Source $EventLogSource -EventID 6556 -EntryType $EventType -Message $LogMessage -Category 1 -ErrorAction Stop
    } catch {
        Write-Warning "Failed to create Event Log entry, trying to create the Event source..."

        if (-not (Test-Administrator)) {
            Write-Error "This script must be executed with Administrator rights ONE time to create the necessary Windows Event Source."
            exit 1
        }
        else {
            if ([System.Diagnostics.EventLog]::SourceExists($EventLogSource) -eq $false) {
                try {
                    New-EventLog -LogName "System" -Source $EventLogSource
                    Write-EventLog -LogName "System" -Source $EventLogSource -EventID 6556 -EntryType $EventType -Message $LogMessage -Category 1 -ErrorAction Stop
                    Write-Host "Event source '$EventLogSource' created successfully."
                } catch {
                    Write-Error "Unable to create Event Source '$EventLogSource' in Windows System Eventlog: $($_.Exception.Message)"
                }
            }
        }
    }
}
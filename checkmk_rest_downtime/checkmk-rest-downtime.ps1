#####################################################
# Set a Host Downtime in checkmk using the REST API #
# Andre.Eckstein@Bechtle.com                        #
#####################################################

##########
# Config #
##########

$CheckmkServer = "192.168.215.11"
$CheckmkSite = "monitoring"
$protocol = "http"

$AutomationUser = "automation"
$AutomationPassword = "12345678910"

$DowntimeDuration = 300
$DowntimeComment = "Downtime Set by downtime script."
$DownTimeFixed = "yes"

$ignore_tls_errors = "yes"

# short|FQDN
$HostnameFormat = "short"

# none | lowercase | uppercase | titlecase
$ConvertCase = "uppercase"

$Debug = $true

$DomainSuffix = ".mydomain.local"

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
        [string]$ConvertCase
	)

    if ( $debug ) {
        write-host "Debug: Hostname conversion - Starting case conversion, conversion mode: $ConvertCase"
    }

    if ( $ConvertCase -eq "lowercase") {
        $hostname = HostnametoLowerCase $hostname
    }
    elseif ( $ConvertCase -eq "uppercase") {
        $hostname = HostnametoUpperCase $hostname
    }
    elseif ( $ConvertCase -eq "titlecase") {
        $hostname = HostnametoTitleCase $hostname
    }
        
    else {
        if ( $debug ) {write-host "Debug: Hostname conversion - Not doing any case conversion, no method choosen"}
    }

    return $hostname
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
    if ( $debug ) {write-host "Debug: Domain Suffix - Not adding a domain suffix. none entered."}
}

if ($ConvertCase -ne "none") {
    $hostname = RewriteHostname $hostname $ConvertCase
}

if ( $debug ) { write-host "Debug: Hostname conversion - Final Hostname after all conversions : $hostname" }

if ($ignore_tls_errors -eq "yes") {

    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
    # Disable SSL verification
}

# Construct http Header

$Header = @{
    'Content-Type' = 'application/json'
    "authorization" = "Bearer $AutomationUser $AutomationPassword"
    'Accept' = 'application/json'
} 

$now = (get-date).ToString("u") 
$datum_ende = (get-date).AddHours(-2).addminutes($TIME).ToString("u") ;
$comment = "Test"

$hostname = "myserver"

$Data =@{  
    start_time = $now;
    end_time =   $datum_ende;
    comment =  $comment;
    host_name = $hostname;
    downtime_type = 'host';
    }  | ConvertTo-Json -Compress

$Parameters = @{
Method = "POST"
Uri = "http://$CheckmkServer/$CheckmkSite/check_mk/api/1.0/domain-types/downtime/collections/host"
Header = $Header
Body = $Data
ContentType = "application/json"
}
 
write-host "http://$CheckmkServer/$CheckmkSite/check_mk/api/1.0/domain-types/downtime/collections/host" 
$result = Invoke-RestMethod @Parameters
write-host $result
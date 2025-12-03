
param (
    [string]$Server,
    [string]$Instance,
    [string]$Hostname,
    [Parameter(Mandatory=$true)]
    [ValidateSet("install", "uninstall", "register_tls", "register_agentupdater", "removehard", "download")]
    [string]$Task,
    [ValidateSet("lowercase", "uppercase", "capitalize")]
    [string]$Case = "lowercase",
    [bool]$UseFQDN = $false,
    [ValidateSet("cleaninstall", "removelegacy", "migratelegacy")]
    [string]$MsiexecType,
    [bool]$IgnoreSSL = $true,
    [ValidateSet("http", "https")]
    [string]$Protocol = "http",

    # CheckMK API Credentials (Default für Automatisierung, kann per Parameter überschrieben werden)
    [string]$Username = "automation",
    [string]$Secret = "WH@IKYGOWPDQSTQEBHBP"
)

#################
# Configuration #
#################

# CheckMK Server und Site (für Automatisierung anpassen)
if (-not $Server)   { $Server = "checkmk.example.com" }
if (-not $Instance) { $Instance = "mysite" }

# Pfade
$DownloadedMSI = "C:\Windows\Temp\check_mk_agent.msi"
$AgentCtlPath = "C:\Program Files (x86)\checkmk\service\cmk-agent-ctl.exe"
$AgentUpdaterPath = "C:\Program Files (x86)\checkmk\service\check_mk_agent.exe"

$ErrorCodes = @{
    1001 = "Fehlende erforderliche Parameter: Server und Instance."
    1002 = "Installation fehlgeschlagen."
    1003 = "Deinstallation fehlgeschlagen."
    1004 = "TLS-Registrierung fehlgeschlagen."
    1005 = "Agent Updater-Registrierung fehlgeschlagen."
    1007 = "API-Anfrage fehlgeschlagen."
    1008 = "Agent-Download fehlgeschlagen."
    1009 = "Fehler beim Abrufen des FQDN."
}

function Get-LocalHostname {
    param (
        [bool]$UseFQDN = $false
    )
    if ($UseFQDN) {
        try {
            $fqdn = [System.Net.Dns]::GetHostEntry($env:COMPUTERNAME).HostName
            return $fqdn
        } catch {
            Write-LogAndExit -ErrorCode 1009 -Message "Fehler beim Abrufen des FQDN: $($_.Exception.Message)"
        }
    } else {
        return $env:COMPUTERNAME
    }
}

function Convert-Hostname {
    param (
        [string]$Hostname,
        [ValidateSet("lowercase", "uppercase", "capitalize")]
        [string]$Case
    )

    switch ($Case) {
        "lowercase" { return $Hostname.ToLower() }
        "uppercase" { return $Hostname.ToUpper() }
        "capitalize" { return -join ($Hostname.Substring(0,1).ToUpper(), $Hostname.Substring(1).ToLower()) }
        default { return $Hostname }
    }
}

function Write-LogAndExit {
    param (
        [int]$ErrorCode,
        [string]$Message
    )
    
    if (-not [System.Diagnostics.EventLog]::SourceExists("CheckmkInstaller")) {
        New-EventLog -LogName Application -Source "CheckmkInstaller"
    }
    $LogMessage = "Fehler $ErrorCode : $Message"
    Write-EventLog -LogName Application -Source "CheckmkInstaller" -EntryType Error -EventId $ErrorCode -Message $LogMessage
    exit $ErrorCode
}

function Download-Agent {
    param (
        [string]$HostName,
        [string]$OsType = "windows_msi"
    )

    # Basis-URL der Checkmk-API
    $ApiUrl = "${Protocol}://$Server/$Instance/check_mk/api/1.0/domain-types/agent/actions/download_by_host/invoke?os_type=$OsType&host_name=$HostName"

    $AuthHeader = "Bearer $Username $Secret"

    $Headers = @{
        "Authorization" = $AuthHeader
        "Accept"        = "application/octet-stream"
    }

    try {
        $InvokeParams = @{
            Uri         = $ApiUrl
            Method      = 'GET'
            Headers     = $Headers
            OutFile     = $DownloadedMSI
            ErrorAction = 'Stop'
        }

        # PowerShell 7+ supports -SkipCertificateCheck
        if ($PSVersionTable.PSVersion.Major -ge 7 -and $IgnoreSSL) {
            $InvokeParams['SkipCertificateCheck'] = $true
        }
        elseif ($IgnoreSSL) {
            # PowerShell 5.x workaround
            [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
        }

        Invoke-RestMethod @InvokeParams

        if (Test-Path -Path $DownloadedMSI) {
            Write-Host "Agent erfolgreich heruntergeladen: $DownloadedMSI"
        } else {
            Write-LogAndExit -ErrorCode 1008 -Message "$($ErrorCodes[1008])"
        }
    } catch {
        Write-Host "Download-Fehler: $($_.Exception.Message)"
        Write-LogAndExit -ErrorCode 1007 -Message "$($ErrorCodes[1007]) Exception: $($_.Exception.Message)"
    }
}

function Install-Agent {

    if (-Not (Test-Path $DownloadedMSI)) {
        write-LogandExit -ErrorCode 1008 -Message "$($ErrorCodes[1008])"
    }
    Execute-Process -Command "msiexec.exe" -Arguments "/i $DownloadedMSI /qn" -ErrorCode 1002
}

function Uninstall-Agent {
    Write-Host "Uninstalling checkmk Agent"
    Execute-Process -Command "msiexec.exe" -Arguments "/x $DownloadedMSI /qn" -ErrorCode 1003
}

function Remove-Hard {
    Write-Host "Uninstalling checkmk agent the hard way"
    Uninstall-Agent
    Remove-Item -Path "C:\ProgramData\checkmk" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "C:\Program Files (x86)\checkmk" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Checkmk Agent vollständig entfernt."
}

function Register-TLS {
    param (
        [string]$HostName,
        [string]$Server,
        [string]$Instance,
        [string]$Username,
        [string]$Secret
    )
    write-host "$AgentCtlPath register --hostname $HostName --server $Server --site $Instance --user $username --password $Secret --trust-cert"
    Execute-Process -Command $AgentCtlPath -Arguments "register --hostname $HostName --server $Server --site $Instance --user $username --password $Secret --trust-cert" -ErrorCode 1004
}

function Register-AgentUpdater {
    param (
        [string]$HostName,
        [string]$Username,
        [string]$Secret
    )
    Execute-Process -Command $AgentUpdaterPath -Arguments "updater register -H $HostName -U $Username -P $Secret -v" -ErrorCode 1005
}

function Execute-Process {
    param (
        [string]$Command,
        [string]$Arguments,
        [int]$ErrorCode
    )
    try {
        $process = Start-Process -FilePath $Command -ArgumentList $Arguments -NoNewWindow -PassThru
        Wait-Process -Id $process.Id
        if ($process.ExitCode -ne 0) {
            Write-LogAndExit -ErrorCode $ErrorCode -Message "$($ErrorCodes[$ErrorCode]) ExitCode: $($process.ExitCode)"
        }
    } catch {
        Write-LogAndExit -ErrorCode $ErrorCode -Message "$($ErrorCodes[$ErrorCode]) Exception: $($_.Exception.Message)"
    }
}

########
# Main #
########

if (-not $Hostname) {
    $Hostname = Get-LocalHostname -UseFQDN $UseFQDN
}
$FormattedHostname = Convert-Hostname -Hostname $Hostname -Case $Case

Write-Host "Hostname: $FormattedHostname | Server: $Server | Site: $Instance"

switch ($Task) {
    "download"             { Download-Agent -Hostname $FormattedHostname }
    "install"              { Install-Agent }
    "uninstall"            { Uninstall-Agent }
    "removehard"           { Remove-Hard }
    "register_tls"         { Register-TLS -Hostname $FormattedHostname -Server $Server -Instance $Instance -Username $Username -Secret $Secret }
    "register_agentupdater" { Register-AgentUpdater -HostName $FormattedHostname -Username $Username -Secret $Secret }
}
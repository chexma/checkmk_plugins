# checkmk Monitoring Agent install script
# Andre Eckstein
# Andre.Eckstein@Bechtle.com

[CmdletBinding(PositionalBinding=$false)]

param (
    [switch]$CleanInstall = $false,
    [switch]$Debug = $false,
    [switch]$Help = $false,
    [switch]$Install = $false,
    [switch]$RegisterAgentUpdater = $false,
    [switch]$RegisterTls = $false,
    [switch]$RemoveAgentInstallationFile = $false,

    [string]$CheckMkServer = "",
    [string]$CheckMkSite = "",
    [string]$RegistrationUser = "",
    [string]$UpdaterUser = "",
    [String]$RegistrationPassword = "",
    [String]$UpdaterPassword = "`"`"",

    [ValidateSet('http', 'https')]
    [String]$protocol = 'https',
    [ValidateSet('lowercase', 'uppercase', 'titlecase')]
    [string]$ConvertCase = "",
    [string]$DomainSuffix = "",
    [string]$CheckMkAgentPackageName = "",
    [string]$CheckMkAgentSourceFolder = "",
    [string]$CheckmkAgentDestinationFolder = ""
)

#################
# configuration #
#################

# This stuff can be manually configured to minimize necessary commandline parameters

#$Servers = Get-Content "C:\temp\hosts.txt"
$Servers = "a","b"

$CheckMkAgentPackageName = "check-mk-agent.msi"
$CheckMkAgentSourceFolder = "c:\checkmk\"
$CheckmkAgentDestinationFolder = "C:\Windows\TEMP\"

########
# code #
########

$CheckMkAgentBinary = 'C:\Program Files (x86)\checkmk\service\check_mk_agent.exe'
$CheckMkControllerBinary = 'c:\Program Files (x86)\checkmk\service\cmk-agent-ctl.exe'
$CheckMKAgentCopySourcePath = $CheckMkAgentSourceFolder + $CheckMkAgentPackageName
$CheckMKAgentCopyDestinationPath = $CheckmkAgentDestinationFolder + $CheckMkAgentPackageName 

#############
# Functions #
########### #
function CreatePowershellSession {
    
    $installsession = New-PSSession -ComputerName $Server -ErrorAction Stop -Verbose -Debug  #-Credential get-credential
    if ( $debug ) {
            write-host "Debug: Sucessfully established Powershell remote session to host $Server"
        }
}

# https://stackoverflow.com/a/38738942

Function Write-Log {
    [CmdletBinding()]
    Param(
    [Parameter(Mandatory=$False)]
    [ValidateSet("INFO","WARN","ERROR","FATAL","DEBUG")]
    [String]
    $Level = "INFO",

    [Parameter(Mandatory=$True)]
    [string]
    $Message,

    [Parameter(Mandatory=$False)]
    [string]
    $logfile
    )

    $Stamp = (Get-Date).toString("yyyy/MM/dd HH:mm:ss")
    $Line = "$Stamp $Level $Message"
    If($logfile) {
        Add-Content $logfile -Value $Line
    }
    Else {
        Write-Output $Line
    }
}

function help {
    write-host "Help:"
    write-host "-----"
    write-host "This script installs and registers the checkmk agent remotely via powershell remote."
    write-host ""
    write-host "To adapt the hostname of the monitored host to its name in checkmk, there are two possible functions:"
    write-host "-domainsuffix <suffix>  :   Add a suffix to the hostname"
    write-host "-convertcase <case>     :   Convert hostname case of remote host to match hostname in checkmk. Possible choices: UPPERCASE,lowercase,Titlecase"
    write-host ""
    write-host "Possible Actions (can be combined)"
    write-host "-install                :   Copy a checkmk install package to the remote server and install it."
    write-host "-registertls            :   Register agent for TLS"
    write-host "-RegisterAgentUpdater   :   Register aent updater plugin"
    write-host "-debug                  :   Show Debug output."
    write-host ""
    write-host "Examples:"
    write-host ".\checkmk_agent_installer.ps1 -install"
    write-host ".\checkmk_agent_installer.ps1 -install -registeragentupdater -registertls -convertcase lowercase"
    write-host ".\checkmk_agent_installer.ps1 -registeragentupdater -registertls -convertcase lowercase -debug"
    write-host ""
    #
    exit 0
}

function AddDomainSuffix {
    [CmdletBinding()]
	param(
		[Parameter(Mandatory)]
		[string]$hostname,
        [string]$DomainSuffix
	)

    if ( $debug ) {
        write-host "Debug: Hostname conversion - Adding domain suffix ""$DomainSuffix"" to hostname"
    }
    # TODO - Remove first . if existent
    # Pseudocode
    # if ($Domainsuffix[0] -eq ".") {
    #     $Domainsuffix[0].Remove()
    # } 
    $hostname = "$hostname.$DomainSuffix"

    return $hostname
}

# get local hostname of the current remote Server
function GetHostnameOfRemoteHost {
    Invoke-Command -Session $installsession -ScriptBlock {
        $local_hostname = ($env:COMPUTERNAME)
        return $local_hostname
    }
}

# construct hostname of the Server
function RewriteHostname {
    [CmdletBinding()]
	param(
		[Parameter(Mandatory)]
		[string]$hostname,
        [string]$convertcase,
        [string]$DomainSuffix
	)

    if ( $debug ) {
        # TODO Bessere Namen auswÄ‚Â¤hlen
        write-host "Debug: Hostname conversion - Hostname in local hosts file: $Server, local hostname on remote server: $hostname"
    }

    if ( $DomainSuffix ) {

        if ( $debug ) {
            write-host "Debug: Hostname conversion - Adding domain suffix enabled"
        }

        $hostname = AddDomainSuffix $hostname $DomainSuffix

        if ( $debug ) {
            write-host "Debug: Hostname conversion - Hostname after adding domain suffix : $hostname"
        }
    }
    else {
        if ( $debug ) {write-host "Hostname conversion - Not adding a domain suffix. none entered."}
    }

    if ( $convertcase ) { 

        if ( $debug ) {
            write-host "Debug: Hostname conversion - Starting case conversion, conversion mode: $convertcase"
        }
    
        if ( $convertcase -eq "lowercase") {
            $hostname = HostnametoLowerCase $hostname
        }
        elseif ( $convertcase -eq "uppercase") {
            $hostname = HostnametoUpperCase $hostname
        }
        elseif ( $convertcase -eq "titlecase") {
            $hostname = HostnametoTitleCase $hostname
        }
        
    }
    else {
        if ( $debug ) {write-host "Hostname conversion - Not doing any case conversion, no method choosen"}
    }

    write-host "Hostname conversion - Final Hostname after all conversions : $hostname"

    return $hostname
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

function CreateHost {
    $API_URL= "https://$HOST_NAME/$CheckMkSite_NAME/check_mk/api/1.0/domain-types/host_config/collections/all"

    $Headers = @{
    "Accept" = "application/json"
    "Authorization" = "Bearer $USERNAME $PASSWORD"
    "Content-Type" = "application/json"
    }
    
#    $body = "{
#    "folder":"~test",
#    "host_name":"myserver1234",
#    "attributes":{
#        "ipaddress":"192.168.0.42",
#        "labels":{
#            "agent": "snmp_v3"
#        }
#    }
#    }"
#
#    Invoke-RestMethod -Method Post -Uri $API_URL -Headers $Headers -Body $body   
}

function DoConnectionTestsOnRemoteHost {
        # Do some basic connectivity checks on the remote host   
    if ( $debug ) {write-host "Debug: Starting basic connectivity tests on host $Server..."}

    Invoke-Command -Session $installsession -ScriptBlock {
    
        if ( $registertls -or $registeragentupdater ) {
            # Test HTTP(s) access to the checkmk Server
	        $check_mk_base_url  = $Using:protocol + "://" + $Using:CheckMkServer + "/" + $Using:CheckMkSite + "/check_mk"

	        try {
	    		$test_connection = Invoke-WebRequest -UseBasicParsing -DisableKeepAlive -Uri $check_mk_base_url -Method 'Head' -ErrorAction 'stop' -TimeoutSec 5
                if ( $Using:debug ) {
                    write-host "Debug: Connectivity tests - Succesfully reached checkmk website at $check_mk_base_url, http response code was" $test_connection.StatusCode
                }
	        } catch {
	    		write-host "Error : Connectivity tests - Unable to connect to check_mk url $check_mk_base_url."
	        }

	        if ( $test_connection.StatusCode -ne 200) {
                write-host "Error: Connectivity tests - Unable to access checkmk at $check_mk_base_url "
                break
	        }
        }
            # Test local and remote file access

        if ( $install) {    
            if ( Test-Path -Path $Using:CheckMKAgentCopySourcePath ) {
                write-host "Debug: Connectivity tests - MSI Installation Package $Using:CheckMKAgentCopySourcePath is accessible"
            }
            else {
                write-host "Error - checkmk Agent MSI Installation Package $Using:CheckMKAgentCopySourcePath is not accessible"
                break
            }

            if ( Test-Path -Path $Using:CheckmkAgentDestinationFolder ) {
                write-host "Debug: Connectivity tests - Copy Destination folder $Using:CheckmkAgentDestinationFolder is accessible"
            }
            else {
                write-host "Error - checkmk Agent Copy Destination folder $Using:CheckMKAgentCopySourcePath is not accessible"
                break
            }
        }    
    }
}

function Check_Current_Deployment_State{
#    $InstalledApplicationsFromRegistry = @() $InstalledApplicationsFromRegistry += Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" # x86 Apps $InstalledApplicationsFromRegistry += Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" # x64 Apps
#    CurrentInstall = $InstalledApplicationsFromRegistry | Where-Object {$_.DisplayName -match $SourceProductName} if ($CurrentInstall.DisplayVersion -eq $SourceProductVersion -or [System.Version]$CurrentInstall.DisplayVersion -ge [System.Version]$SourceProductVersion) {
}

# Test if checkmk binaries are installed
function is_checkmk_agent_installed {
    Invoke-Command -Session $installsession -ScriptBlock {
        if (-not( Test-Path -Path $CheckMkAgentBinary -Leaf) -or -not( Test-Path -Path $CheckMkControllerBinary -Leaf))  {
            write-host "checkmk agent is not installed in the given path"
            return false
        }
    }
}

# Copy Agent to monitored Host
function CopyCheckmkAgent {
    write-host "Agent Installation - Starting to copy checkmk Agent to remote host $Server"
    Copy-Item $CheckMKAgentCopySourcePath -Destination $CheckmkAgentDestinationFolder -ToSession $installsession
    Invoke-Command -Session $installsession -ScriptBlock {
        
        if ( $Using:debug ) {
            write-host "Debug: Agent Installation - Copying checkmk agent from $Using:CheckMKAgentCopySourcePath to $Using:CheckmkAgentDestinationFolder on $Using:Server."
        }

        $StartTime = Get-Date
        #Copy-Item -Path $Using:CheckMKAgentCopySourcePath -Destination $Using:CheckmkAgentDestinationFolder
        
        if ( $LASTEXITCODE -gt 0) { 
            write-host "Error: Agent Installation - Failed to copied the check_MK Agent to $Using:CheckmkAgentDestinationFolder on $Using:Server."
            break
        }
        else { 
            if ( $Using:debug ) {
                write-host "Debug: Agent Installation - Successfully copied check_MK Agent to $Using:CheckmkAgentDestinationFolder on $Using:Server. The download took $((Get-Date).Subtract($StartTime).Seconds) second(s)"
            }
        }
    }
}

# Install checkmk Agent
function InstallCheckmkAgent {   
    write-host "Agent Installation - Installing checkmk Agent on $Server"
    Invoke-Command -Session $installsession -ScriptBlock { 
    
    $MSIInstallParameters = @('/I', $Using:CheckMKAgentCopyDestinationPath, '/quiet', '/norestart', '/qn' )
    $MSIInstallResult = Start-Process msiexec.exe -Wait -PassThru -ArgumentList $MSIInstallParameters
    $MSIInstallExitCode = $MSIInstallResult.ExitCode

    if ( $MSIInstallExitCode -eq 0) { 
        write-host "Agent Installation - MSI Installation of $Using:CheckMKAgentCopyDestinationPath succesfull"
    } 
    else {
        write-host "unsuccessfull"
    }
    }
}

# register agent updater
function RegisterAgentUpdater {
    [CmdletBinding()]
	param(
		[Parameter(Mandatory)]
		[string]$hostname
    )

    write-host "Registering checkmk agent updater plugin on $Server "
    Invoke-Command -Session $installsession -ScriptBlock {
        
        # TODO Variable
        if (-not( Test-Path -Path "C:\Program Files (x86)\checkmk\service\check_mk_agent.exe" -PathType Leaf)) {
            write-host "checkmk is not installed in the given path."
            break
        }

        if ( $Using:debug ) {
            write-host "Debug: Register Agent Updater - Register hostname is" $Using:hostname
        }

        $agent_updater_parameters = @('updater', 'register','-H',$Using:hostname,'-U',$Using:UpdaterUser,'-P',$Using:UpdaterPassword,'-v')
        if ( $Using:debug) {
            write-host "Debug: Full agent updater plugin command = $Using:CheckMkAgentBinary $agent_updater_parameters"
        }
		$register_updater_register_result = & $Using:CheckMkAgentBinary $agent_updater_parameters 2>&1   
        
        if ( $LASTEXITCODE -eq 0 ) {
            write-host "Debug: Register Agent Updater - Agent Updater registered successfully..."
            if ( $Using:debug) {
                write-host "Debug: Register Agent Updater - Output of Agent Updater command:"
                write-host ""
                write-host $register_updater_register_result|Out-String
                write-host ""
            }
        }    
        else {
            write-host "Debug: Register Agent Updater - failed to register agent updater"
            write-host "Debug: Register Agent Updater - Output :" 
            write-host $register_updater_register_tls_result
        }
    }
}

# register agent controller tls 
function RegisterTls {
    [CmdletBinding()]
	param(
		[Parameter(Mandatory)]
		[string]$hostname
	)

    write-host "Registering checkmk Agent TLS"

    Invoke-Command -Session $installsession -ScriptBlock {

        if (-not( Test-Path -Path $Using:CheckMkControllerBinary -PathType Leaf)) {
            write-host "Error: Register agent TLS - checkmk agent controller binary is not installed in the given path."
            break
        }

        $agent_register_tls_parameters = @('register', '-s', $Using:CheckMkServer,'-i', $Using:CheckMkSite , '-H', $Using:hostname , '-U', $Using:RegistrationUser , '-P', $Using:RegistrationPassword, '--trust-cert')
        
        if ( $Using:debug ) {
            write-host "Debug: Register agent TLS - Full register tls command = $Using:CheckMkControllerBinary $agent_register_tls_parameters"
        }

        $register_updater_register_tls_result = & $Using:CheckMkControllerBinary $agent_register_tls_parameters 2>&1
        
        if ( $LASTEXITCODE -eq 0 ) {
            write-host "Registering agent tls successfull."
        } 
        else {    
            write-host "Error : Failed to register agent tls"
            write-host "Output of agent register tls command :"
            write-host "..."
            write-host $register_updater_register_tls_result
            write-host "..."
        }
    }
}

# force agent updater refresh
function ForceRefreshOfAgentUpdater {
    # Force Update to the correct checkmk agent immediately
    write-host "Forcing Agent Updater Refresh..."
    Invoke-Command -Session $installsession -ScriptBlock {

        $agent_updater_parameters = @('updater', '-vf')
        if ( $Using:debug ) {
            write-host "Debug: Register Agent Updater - Full agent updater refresh command = $Using:CheckMkAgentBinary $agent_updater_parameters"

        $register_updater_refresh_result = & $Using:CheckMkAgentBinary $agent_updater_parameters 2>&1
        }

        If ( $LASTEXITCODE -eq 0 ) {
            if ( $Using:debug) {
                write-host "Debug: Register Agent Updater - Successfully refreshed agent updater" 
            }
            else { 
                    write-host "failed to refresh agent updater:"
                    write-host "$register_updater_refresh_result"
            }
        }
    }
}

# remove Agent installation package
function RemoveAgentMSIFile { 
    Invoke-Command -Session $installsession -ScriptBlock {
        if ($Using:Debug) { write-host "Debug: Agent Installation - Deleting checkmk agent installation MSI File $Using:CheckmkAgentDestinationFolder\$Using:CheckMkAgentPackageName on Server $Server"}
        
        Remove-Item -Path "$Using:CheckmkAgentDestinationFolder\$Using:CheckMkAgentPackageName"
        
        If ( $LASTEXITCODE -eq 0 ) {
            if ( $Using:debug) {
                write-host "Debug: Agent Installation - Succesfully deleted checkmk agent installation MSI File" 
            }
        else { 
                write-host "Debug: Agent Installation - failed to delete $Using:CheckmkAgentDestinationFolder\$Using:CheckMkAgentPackageName"
            }
        }

    }    
}

########
# MAIN #
########

if ( $help) { help }

foreach ($Server in $Servers)
    {
    
    $installsession = New-PSSession -ComputerName $Server -ErrorAction Stop -Verbose -Debug  #-Credential get-credential
    
   
    $hostname = GetHostnameOfRemoteHost
    $hostname = RewriteHostname $hostname $convertcase $DomainSuffix
        
    DoConnectionTestsOnRemoteHost

    if ( $install ){
        CopyCheckmkAgent
        InstallCheckmkAgent
    }
   
    if ( $RemoveAgentInstallationFile ){
        RemoveAgentMSIFile
    }

    if ( $RegisterAgentUpdater ){
        RegisterAgentUpdater $hostname
        ForceRefreshOfAgentUpdater
    }
    
    if ( $registertls ){
        RegisterTls $hostname
    }

    # Exit-PSSession
}

# TODO
# - Function for getting hosts / reading hostfiles
# - get-credential benutzen
# - check if checkmk is already installed ?
# - MSI Parameter enter ( Clean Install etc. ) 
# - Difference between v2.0 und v2.1 ? Variables ?
# - process {} necessary ?

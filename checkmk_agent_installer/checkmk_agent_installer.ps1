# yacai - yet another agent installer
# checkmk Monitoring Agent install script
# Andre Eckstein
# Andre.Eckstein@Bechtle.com

param (
    [string]$CheckMkServer = "192.168.215.11",
    [string]$CheckMkSite = "monitoring",
    [string]$RegistrationUser = "cmkadmin",
    [String]$RegistrationPassword = "password",
    [switch]$registertls = $false,
    [switch]$install = $false,
    [switch]$registeragentupdater = $false,
    [switch]$debug = $false,
    [switch]$remove_tmp_file = $false,
    [switch]$help = $false,
    [switch]$convertcase = $false
)

#################
# configuration #
#################

# This stuff has to be configured

#$Servers = Get-Content "C:\temp\hosts.txt"
$Servers = 'localhost'
#$CheckMkAgentFile = "\\srv-iuk\d$\IuK\ProgrammKatalog\check_mk\Programm\Aktueller_Client\check-mk-agent21.msi"

#
$CheckMkAgentPackageName = "check-mk-agent21.msi"
$CheckMkAgentSourceFolder = "c:\\temp\"
$CheckmkAgentDestinationFolder = "\\$Server\C$\Windows\TEMP\"

#$RegistrationUser = "cmkadmin"
$RegistrationPassword = "password"

# This stuff can be configured
$checkmk_agent_binary = 'C:\Program Files (x86)\checkmk\service\check_mk_agent.exe'
$checkmk_controller_binary = 'C:\ProgramData\checkmk\agent\bin\cmk-agent-ctl.exe'
#$remove_tmp_file = "yes"
$CheckmkTransportProtokoll = "http"

# Hostname Conversion
$hostname_convert_function = "lowercase" # lowercase | UPPERCASE | Pascalcase

#TODO $hostname_type = fqdn,short

########
# code #
########

# Functions

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

# construct hostname of the Server
function rewrite_hostname {
    Invoke-Command -Session $session -ScriptBlock {
        $hostname = ($env:COMPUTERNAME).ToLower()
        return $hostname
    }
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

function Check_CheckMkSite_Accessibility {
        # Do some connectivity testing on the remote host
        if ( $Using:debug) {write-host "Debug: Testing Connectivity..."}
    Invoke-Command -Session $session -ScriptBlock {
	    $check_mk_base_url  = $Using:CheckmkTransportProtokoll + "://" + $Using:CheckMkServer + "/" + $Using:CheckMkSite + "/check_mk"
        if ( $Using:debug ) {
            write-host "Debug : checkmk Base URL is $check_mk_base_url"
        }

	    try {
			$test_connection = Invoke-WebRequest -UseBasicParsing -DisableKeepAlive -Uri $check_mk_base_url -Method 'Head' -ErrorAction 'stop' -TimeoutSec 5
            if ( $Using:debug ) {
                write-host "Debug : Succesfully reached $check_mk_base_url"
            }
	    } catch {
			write-host "Error : Unable to connect to check_mk url $check_mk_base_url."
	    }

        if ( $Using:debug ) {
            write-host "Debug : http response code was $test_connection.StatusCode"
        }
	
	    if ( $test_connection.StatusCode -ne 200) {
            break
	    }
    }
}

function Check_Current_Deployment_State{

}

# Test if checkmk binaries are installed
function is_checkmk_agent_installed {
    Invoke-Command -Session $session -ScriptBlock {
        if (-not( Test-Path -Path $checkmk_agent_binary -Leaf) -or -not( Test-Path -Path $checkmk_controller_binary -Leaf))  {
            write-host "checkmk agent is not installed in the given path"
            return false
        }
    }
}

# Copy Agent to monitored Host
function CopyCheckmkAgent {
    write-host "Copying checkmk Agent to $Server"
    Invoke-Command -Session $session -ScriptBlock {
        $source_path = $Using:CheckMkAgentSourceFolder + $Using:CheckMkAgentPackageName
        $dest_path = $Using:CheckmkAgentDestinationFolder + $Using:CheckMkAgentPackageName
        
        if ( $Using:debug )
            {
            write-host "Debug: checkmk Agent Source Path: $source_path"
            write-host "Debug: checkmk Agent Dest Path: $dest_path"
            }
        
        $StartTime = Get-Date
        Copy-Item -Path $source_path -Destination $dest_path
        if ( $LASTEXITCODE -gt 0 -and $Using:debug )
            {
            write-host "Debug: Successfully copied the check_MK Agent to $dest_path. The download took $((Get-Date).Subtract($StartTime).Seconds) second(s)"
            }
        }
}

# Install checkmk Agent
function InstallCheckmkAgent {   
    write-host "Installing checkmk Agent on $Server"
    Invoke-Command -Session $session -ScriptBlock { 
    # TODO Pfad in Variable umschreiben
    Start-Process msiexec.exe -Wait -ArgumentList '/I C:\Windows\TEMP\check-mk-agent21.msi /quiet /norestart'
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
    Invoke-Command -Session $session -ScriptBlock {
        
        if (-not( Test-Path -Path "C:\Program Files (x86)\checkmk\service\check_mk_agent.exe" -PathType Leaf)) {
            write-host "checkmk is not installed in the given path."
            break
        }
# TODO convert functions for upper and lower case
        #$hostname = ($env:COMPUTERNAME).ToLower()
        #$hostname  = $Using:rewrite_hostname
# TODO check for Secret or password

        if ( $Using:debug ) {
            write-host "Debug: local Server hostname is" $hostname
        }

        $agent_updater_parameters = @('updater', 'register','-H',$hostname,'-U',$Using:RegistrationUser,'-P',$Using:RegistrationPassword,'-v')
        if ( $Using:debug) {
            write-host "Debug: Full agent updater plugin command = $Using:checkmk_agent_binary $agent_updater_parameters"
        }
		$register_updater_register_result = & $Using:checkmk_agent_binary $agent_updater_parameters 2>&1   
        
        if ( $Using:debug) {
            write-host "Output of Agent Updater :"
            write-host "..."
            write-host $register_updater_register_result|Out-String
            write-host "..."
        }

        # TODO Write-Log
        If ( $LASTEXITCODE -gt 0 )
            {
            #Write-Log WARN $(Get-Date -Format G) "cmk Update Agent Registration Failed"
            #Write-Log WARN $(Get-Date -Format G) $register_updater_register_result
            } else {
           #Write-Log INFO  $(Get-Date -Format G) "cmk Update Agent Plugin Registration succesfull"
        }

        if ( $LASTEXITCODE -gt 0 )
        {
            write-host "failed to register agent tls"
            write-host "output : $register_updater_register_tls_result"
        } else {
            write-host "Agent Updater registered successfully..."
        }

    }
}

# register agent controller tls 
function RegisterTls {
    # TODO get HOSTNAME from function
    write-host "Registering checkmk Agent TLS"

    Invoke-Command -Session $session -ScriptBlock {

        if (-not( Test-Path -Path $Using:checkmk_controller_binary -PathType Leaf)) {
            write-host "checkmk agent controller binary is not installed in the given path."
        }
        $hostname = ($env:COMPUTERNAME).ToLower()
        #$argument = "register -s $Using:cmkserver1 -i $Using:site -H $hostname -U $Using:registration_user -P $Using:registration_secret --trust-cert"
        $agent_register_tls_parameters = @('register', '-s', $Using:CheckMkServer,'-i', $Using:CheckMkSite , '-H', $hostname , '-U', $Using:RegistrationUser , '-P', $Using:RegistrationPassword, '--trust-cert')
        if ( $Using:debug ) {
            write-host "Debug: Full register tls command = $Using:checkmk_controller_binary $agent_register_tls_parameters"
        }

        $register_updater_register_tls_result = & $Using:checkmk_controller_binary $agent_register_tls_parameters 2>&1
        
        
        if ( $LASTEXITCODE -gt 0 )
        {
            write-host "failed to register agent tls"
            write-host "output : $register_updater_register_tls_result"
        } else {
            write-host "Registering agent tls successfull"
            if ($Using:debug) {write-host "Output of TLS register command : $register_updater_register_tls_result"}
        }

    }
}

# force agent updater refresh
function force_refresh_of_agent_updater {
    # Update to the correct agent version immediately
    write-host "Forcing Agent Updater Refresh..."
    Invoke-Command -Session $session -ScriptBlock {

        $agent_updater_parameters = @('updater', '-vf')
        if ( $Using:debug ) {
            write-host "Debug: full agent updater refresh command = $Using:checkmk_agent_binary $agent_updater_parameters"

        $register_updater_refresh_result = & $Using:checkmk_agent_binary $agent_updater_parameters 2>&1
        }

        If ( $LASTEXITCODE -gt 0 )
            {
                write-host "failed to refresh agent updater"
                write-host "output : $register_updater_refresh_result"
        }
        else { 
            if ( $Using:debug) {
                write-host "Successfully refreshed agent updater" 
            }
        }
    }
}

# remove Agent installation package
function remove_agent_installation_file { 
#    Invoke-Command -Session $session -ScriptBlock {
#
#        write-host "Removing Temp File on Server"
#            # TODO Test
#            Remove-Item -Path "$Using:$CheckmkAgentDestinationFolder\$CheckMkAgentPackageName"
#    }
}

########
# MAIN #
########

foreach ($Server in $Servers)
    {
    
    write-host "################################"
    write-host "    Current Server: $Server"
    write-host "################################"
    
    try {
        $session = New-PSSession -ComputerName $Server -ErrorAction Stop #-Credential get-credential
    }
    catch {
        write-host "Error : unable to create Powershell Session"
        break
    }
    
    Check_CheckMkSite_Accessibility

    $final_hostname = rewrite_hostname
    
    if ( $debug ) {
        write-host "Debug: Hostname in local file: $Server"
        write-host "Debug: Final (rewritten) Hostname: $final_hostname"
    }

    if ( $install ){

        CopyCheckmkAgent
        InstallCheckmkAgent
    }
   
    if ( $remove_tmp_file ){
        remove_agent_installation_file
    }

    if ( $registeragentupdater ){
        RegisterAgentUpdater $final_hostname
        force_refresh_of_agent_updater
    }
    
    if ( $registertls ){
        RegisterTls $final_hostname
    }
    
    Exit-PSSession
}

# TODO
# - Web Tests zum prüfen ob CheckMkSite erreichbar, wenn tls oder agent updater oder register
# - get-credential benutzen
# - Rewrite Functions
# - Parametrisierung für jeden Befehl
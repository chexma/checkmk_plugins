# checkmk Agent install script
# Andre Eckstein
# Andre.Eckstein@Bechtle.com

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

# checkmk Server specific stuff
$CheckMkServer="192.168.215.11"
$CheckMkSite="monitoring"
$RegistrationUser = "cmkadmin"
$RegistrationSecret = "password"

# What to do 
$InstallCheckmkAgent = "yes"
$AgentRegisterTLS = "yes"
$AgentRegisterUpdater = "yes"
$AddHostTocheckmk = "yes"

# This stuff can be configured
$checkmk_agent_binary = 'C:\Program Files (x86)\checkmk\service\check_mk_agent.exe'
$checkmk_controller_binary = 'C:\ProgramData\checkmk\agent\bin\cmk-agent-ctl.exe'
$remove_tmp_file = "yes"
$debug = "yes"
$CheckmkTransportProtokoll = "http"

# Hostname Conversion
$hostname_convert_function = "lowercase" # lowercase | uppercase 

#TODO $hostname_type = short,long

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
    write-host "Debug: constructing hostname on $Server"
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
    
    $body = "{
    "folder":"~test",
    "host_name":"myserver1234",
    "attributes":{
        "ipaddress":"192.168.0.42",
        "labels":{
            "agent": "snmp_v3"
        }
    }
    }"

    Invoke-RestMethod -Method Post -Uri $API_URL -Headers $Headers -Body $body   
}

function Check_CheckMkSite_Accessibility {
        # Do some connectivity testing 
    Invoke-Command -Session $session -ScriptBlock {
	    $check_mk_base_url  = $Using:CheckmkTransportProtokoll + "://" + $Using:CheckMkServer + "/" + $Using:CheckMkSite + "/check_mk"
        if ( $debug -eq "yes") {
            write-host "Debug : checkmk Base URL is $check_mk_base_url "
        }

	    try {
			$test_connection = Invoke-WebRequest -UseBasicParsing -DisableKeepAlive -Uri $check_mk_base_url -Method 'Head' -ErrorAction 'stop' -TimeoutSec 5
	    } catch {
			write-host "Error : Unable to connect to check_mk url $check_mk_base_url."
	    }

        if ( $debug -eq "yes") {
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
        
        if ( $debug = "yes")
            {
            write-host "Debug: checkmk Agent Source Path: $source_path"
            write-host "Debug: checkmk Agent Dest Path: $dest_path"
            }
        }
        $StartTime = Get-Date
        Copy-Item -Path $source_path -Destination $dest_path
        if ( $LASTEXITCODE -gt 0 -and $debug = "yes")
            {
            write-host "Debug: Successfully copied the check_MK Agent to $dest_path. The download took $((Get-Date).Subtract($StartTime).Seconds) second(s)"
            }
        }
}

# Install checkmk Agent
function InstallCheckmkAgent {   
    write-host "Installing checkmk Agent on $Server"
    Invoke-Command -Session $session -ScriptBlock { 
    # TODO
    Start-Process msiexec.exe -Wait -ArgumentList '/I C:\Windows\TEMP\check-mk-agent21.msi /quiet /norestart'
    }
}

# register agent updater
function AgentRegisterUpdater {
    [CmdletBinding()]
	param(
		[Parameter(Mandatory)]
		[string]$hostname
	)

    write-host "--- Registering checkmk agent updater plugin on $Server ---"
    Invoke-Command -Session $session -ScriptBlock {
        
        if (-not( Test-Path -Path "C:\Program Files (x86)\checkmk\service\check_mk_agent.exe" -PathType Leaf)) {
            write-host "checkmk is not installed in the given path."
            break
        }
# TODO convert functions for upper and lower case
        #$hostname = ($env:COMPUTERNAME).ToLower()
        #$hostname  = $Using:rewrite_hostname
# TODO check for Secret or password

        if ( $debug = "yes") {
            write-host "Debug: local Server hostname is" $hostname
        }

        $agent_updater_parameters = @('updater', 'register','-H',$hostname,'-U',$Using:RegistrationUser,'-P',$Using:RegistrationSecret,'-v')
        if ( $debug = "yes") {
            write-host "Debug: Full agent updater plugin command = $Using:checkmk_agent_binary $agent_updater_parameters"
        }
		$register_updater_register_result = & $Using:checkmk_agent_binary $agent_updater_parameters 2>&1   
        
        write-host $register_updater_register_result

        If ( $LASTEXITCODE -gt 0 )
            {
            #Write-Log WARN $(Get-Date -Format G) "cmk Update Agent Registration Failed"
            #Write-Log WARN $(Get-Date -Format G) $register_updater_register_result
            } else {
           #Write-Log INFO  $(Get-Date -Format G) "cmk Update Agent Plugin Registration succesfull"
        }
    }
}

# register agent controller tls 
function RegisterTls {
    write-host "--- Registering checkmk Agent TLS on $Server ---"

    Invoke-Command -Session $session -ScriptBlock {

        if (-not( Test-Path -Path "C:\ProgramData\checkmk\agent\bin\cmk-agent-ctl.exe" -PathType Leaf)) {
            write-host "checkmk agent controller is not installed in the given path."
        }
        $hostname = ($env:COMPUTERNAME).ToLower()
        $agent_register_tls_parameters = @('register', '-s', $Using:CheckMkServer,'-i', $Using:CheckMkSite , '-H', $hostname , '-U', $Using:RegistrationUser ,'--trust-cert')
        if ( $debug = "yes") {
            write-host "Debug: Full agent updater plugin command = $Using:checkmk_agent_binary $agent_register_tls_parameters"
        }

        $register_updater_register_tls_result = & $Using:checkmk_agent_binary $agent_updater_parameters 2>&1
        
        
        if ( $LASTEXITCODE -gt 0 )
        {
            write-host "failed to register agent tls"
            write-host "output : $register_updater_register_tls_result"
        } else {
            write-host "Registering agent tls successfull"
        }

    }
}

# force agent updater refresh
function force_refresh_of_agent_updater {
    # Update to the correct agent version immediately
    Invoke-Command -Session $session -ScriptBlock {

        $agent_updater_parameters = @('updater', '-vf')
        if ( $debug = "yes") {
            write-host "Debug: full agent updater refresh command = $Using:checkmk_agent_binary $agent_updater_parameters"

        $register_updater_refresh_result = & $Using:checkmk_agent_binary $agent_updater_parameters 2>&1
        }

        If ( $LASTEXITCODE -gt 0 )
            {
                write-host "failed to refresh agent updater"
                write-host "output : $register_updater_refresh_result"
        }
    }
}

# remove Agent installation package
function remove_agent_installation_file { 
#    Invoke-Command -Session $session -ScriptBlock {
#
#        write-host "Removing Temp File on Server"
#            # TODO
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
    Check_CheckMkSite_Accessibility

    $session = New-PSSession -ComputerName $Server #-Credential get-credential
    
    $final_hostname = rewrite_hostname
    
    if ( $debug -eq "yes" ) {
        write-host "Debug: Hostname in local file: $Server"
        write-host "Debug: Final (rewritten) Hostname: $local_server_hostname"
    }

    if ( $InstallCheckmkAgent -eq "yes"){

        CopyCheckmkAgent
        InstallCheckmkAgent
    }
   
    if ( $remove_tmp_file -eq "yes"){
        remove_agent_installation_file
    }

    if ( $AgentRegisterUpdater -eq "yes"){
        AgentRegisterUpdater $final_hostname
        force_refresh_of_agent_updater
    }
    
    if ( $AgentRegisterTLS -eq "yes"){
        RegisterTls
    }
    
    Exit-PSSession
}

# TODO
# - Web Tests zum prüfen ob CheckMkSite erreichbar, wenn tls oder agent updater oder register
# - get-credential benutzen
# - Rewrite Functions
# checkmk Agent install script
# Andre Eckstein
# Andre.Eckstein@Bechtle.com

##################
# general config #
##################

# This stuff has to be configured

#$servers = Get-Content "C:\temp\hosts.txt"
$servers = 'localhost'
#$checkmk_agent_file = "\\srv-iuk\d$\IuK\ProgrammKatalog\check_mk\Programm\Aktueller_Client\check-mk-agent21.msi"
$checkmk_agent_file = "c:\\temp\check-mk-agent21.msi"
$checkmk_server="192.168.215.11"
$site="monitoring"
$registration_user = "cmkadmin"
$registration_secret = "password"

$install_checkmk_agent = "no"
$register_agent_tls = "true"
$register_agent_updater = "true"
 

##########
# config #
##########

# This stuff can be configured
#$destinationFolder = "\\$server\C$\Windows\TEMP"
#$destinationFolder = "\\$server\C$\Windows\TEMP"
$checkmk_agent_binary = 'C:\Program Files (x86)\checkmk\service\check_mk_agent.exe'
$checkmk_controller_binary = 'C:\ProgramData\checkmk\agent\bin\cmk-agent-ctl.exe'
$remove_tmp_file = "false"
$debug = "true"

#TODO $hostname_convert_case = "lower"
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

# construct hostname of the server
function construct_hostname{
    Invoke-Command -Verbose -ComputerName $server -ScriptBlock {
        write-host "Debug: constructing hostame on server $server"
    $hostname = ($env:COMPUTERNAME).ToLower()
    return $hostname
    }
}

function check_current_deployment_state{

}

# Test if checkmk binaries are installed
function is_checkmk_agent_installed {
    if (-not( Test-Path -Path $checkmk_agent_binary -Leaf) -or -not( Test-Path -Path $checkmk_controller_binary -Leaf)  {
        write-host "checkmk agent is not installed in the given path"
        return false
    }
}

# Copy Agent to monitored Host
function copy_checkmk_agent {
    write-host "Copying checkmk Agent to server"
    Copy-Item -Path $checkmk_agent_file -Destination $destinationFolder
}

# Install checkmk Agent
function install_checkmk_agent {    
    write-host "Installing checkmk Agent on server"
    Invoke-Command -ComputerName $server -ScriptBlock {
        Start-Process msiexec.exe -Wait -ArgumentList '/I C:\Windows\TEMP\check-mk-agent21.msi /quiet'
    }
}

# register agent updater
function register_agent_updater {
    Invoke-Command -Verbose -ComputerName $server -ScriptBlock {
        write-host "--- Registering checkmk agent updater plugin on server $server ---"
        if (-not( Test-Path -Path "C:\Program Files (x86)\checkmk\service\check_mk_agent.exe" -PathType Leaf)) {
            write-host "checkmk is not installed in the given path."
            break
        }
# TODO convert functions for upper and lower case
        $hostname = ($env:COMPUTERNAME).ToLower()
        #$hostname  = $Using:construct_hostname
# TODO check for Secret or password

        if ( $debug = "true") {
            write-host "Debug: local server hostname is" $hostname
        }

        $agent_updater_parameters = @('updater', 'register','-H',$hostname,'-U',$Using:registration_user,'-P',$Using:registration_secret,'-v')
        if ( $debug = "true") {
            write-host "Debug: Full agent updater plugin command = " $Using:checkmk_agent_binary $updater_argument
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

# force agent updater refresh
function force_refresh_of_agent_updater {
    # Update to the correct agent version immediately
    Invoke-Command -Verbose -ComputerName $server -ScriptBlock {

        $agent_updater_parameters = @('updater', '-vf')
        if ( $debug = "true") {
            write-host "Debug: full agent updater refresh command = " $Using:checkmk_agent_binary $agent_updater_parameters

        $register_updater_refresh_result = & $Using:checkmk_agent_binary $agent_updater_parameters 2>&1
     
        }
        If ( $LASTEXITCODE -gt 0 )
            {
                write-host "failed to refresh agent updater"
                write-host "output : $register_updater_refresh_result"
        }
    }
    
}

# register agent controller tls 
function register_tls {
    Invoke-Command -Verbose -ComputerName $server -ScriptBlock {
        write-host "- Registering checkmk Agent TLS on server"
        if (-not( Test-Path -Path "C:\ProgramData\checkmk\agent\bin\cmk-agent-ctl.exe" -PathType Leaf)) {
            write-host "checkmk agent controller is not installed in the given path."
        }
        $hostname = ($env:COMPUTERNAME).ToLower()
        $agent_register_tls_parameters = @('register', '-s','$Using:checkmk_server','-i', $Using:site , '-H', $hostname , '-U' $Using:registration_user ,'--trust-cert')
        if ( $debug = "true") {
            write-host "Debug: Full agent updater plugin command = " $Using:checkmk_agent_binary $agent_register_tls_parameters
        $register_updater_register_tls_result = & $Using:checkmk_agent_binary $agent_updater_parameters 2>&1
        }
        
        If ( $LASTEXITCODE -gt 0 )
        {
            write-host "failed to register agent tls"
            write-host "output : $register_updater_register_tls_result"
        } else {
            write-host "Registering agent tls successfull"
        }

    }
}

# remove Agent installation package
function remove_agent_installation_file{ 
    write-host "Removing Temp File on server"
    Invoke-Command -ComputerName $server -ScriptBlock {
        Remove-Item -Path C:\Windows\TEMP\check-mk-agent21.msi
    }
}

foreach ($server in $servers)
    {
    
    write-host "################################"
    write-host "#### Current server: $server ###"
    write-host "################################"


    $local_server_hostname = construct_hostname
    write-host $local_server_hostname

    if ( $install_checkmk_agent -eq "true"){

        copy_checkmk_agent
        install_checkmk_agent
        Start-Sleep -Seconds 10
    }

#    $is_checkmk_agent_installed == is_checkmk_agent_installed
   
    if ( $remove_tmp_file -eq "true"){
        remove_agent_installation_file
    }

    if ( $register_agent_updater -eq "true"){
        register_agent_updater
        force_refresh_of_agent_updater
    }
    
    if ( $register_agent_tls -eq "true"){
        register_tls
    }
    
}
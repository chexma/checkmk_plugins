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

$install_checkmk_agent = "true"
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


#TODO $hostname_convert_case = "lower"
#TODO $hostname_type = short,long

########
# code #
########

# Functions

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
        write-host "Registering checkmk Agent Updater on server" $server
        if (-not( Test-Path -Path "C:\Program Files (x86)\checkmk\service\check_mk_agent.exe" -PathType Leaf)) {
            write-host "checkmk is not installed in the given path."
            break
        }
        $hostname = ($env:COMPUTERNAME).ToLower()
# TODO check for Secret or password
        $updater_argument = "updater register -H $hostname -U $Using:registration_user -P $Using:registration_secret"
        write-host "local hostname" $hostname
        write-host $updater_argument
        Start-Process 'C:\Program Files (x86)\checkmk\service\check_mk_agent.exe' -ArgumentList $updater_argument -Wait -Verbose -NoNewWindow
    }
}

# force agent updater refresh
function force_refresh_of_agent_updater {
    # Update to the correct agent version immediately
    Invoke-Command -Verbose -ComputerName $server -ScriptBlock {
        $argument = "updater -vf"
        Start-Process 'C:\Program Files (x86)\checkmk\service\check_mk_agent.exe' -ArgumentList $argument -Wait -Verbose -NoNewWindow
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
        $tls_argument = "register -s $Using:checkmk_server -i $Using:site -H $hostname -U $Using:registration_user -P $Using:registration_secret --trust-cert"
        Start-Process 'C:\ProgramData\checkmk\agent\bin\cmk-agent-ctl.exe' -ArgumentList $tls_argument -Wait -Verbose -NoNewWindow
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

    write-host "#### Current server: $server ###"

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
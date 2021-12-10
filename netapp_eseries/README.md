# checkmk plugin to monitor Netapp E-Series Storage Systems with checkmk 2.x

How to Install and Configure this checkmk Plugin :

## 1. Installation 

### 1.1 checkmk RAW Edition

- Download the latest checkmk mkp package netapp_eseries-version.mkp
- Copy the file to your checkmk server, e.g. to /tmp
- Make sure that the file is accessible by the "site user" of your monitoring site : `chown <site name> /tmp/netapp_eseries-<version>.mkp`
- Switch to your site user with `su - <your_site_name>`
- Change into the folder where you downloaded checkmk, e.g. `cd /tmp`
- Install the package with `mkp install ./netapp_eseries-<version>.mkp`
- You can check if the package was successfully installed with the command `mkp list`
- After the installation of the mkp you can delete the package file

More Informations about installing mkps on the command line:
https://docs.checkmk.com/latest/en/mkps.html#_installation_of_an_mkp

### 1.2 checkmk Enterprise, Free and Managed Services Edition

- Download the latest checkmk mkp package netapp_eseries-version.mkp
- Open the checkmk Webinterface, select "Setup" - "Extension packages"
- If the entry "Extension packages" is not shown, click on "show more" on the top right of the setup menu
- Select "Upload package"
- Select the downloaded file and "Upload & install"

More Informations about installing mkps in the checkmk webinterface:
https://docs.checkmk.com/latest/en/mkps.html#wato

## 2. Configuration

### 2.1 NetApp E-Series User
Unfortunately it is not possible to create users on the E-Series, therefore we do have to stick with the existing ones.
I would recommend to use the user "monitor" instead of the admin user.
In the webinterface of the E-Series you can easily set a password for that user.

## 2.2 Setup a rule 

- First you have to create a host (your NetApp E-Series) in checkmk
- Enter the necessary values
- Choose "Checkmk agent / API integrations: Configured API integrations, no checkmk agent"
- Select "Save & go to folder"
- Select "Setup - Agents - Other Integrations - Netapp E-Series via REST API"
- Select "Create rule in folder"

The minimum required options are "Username" and "Password", all other options are optional and should not be touched in standard environments.
In "Conditions" either choose the explicit hostname of the host you added beforehands or use other conditions e.g. tags or labels (if defined ) to match your storage system(s).

## 3. Debugging

Login to your checkmk server and switch to the site user (site user has the name of your checkmk site)

### 1. Test connection with curl

`curl -v https://IP-Address-of-Eseries:8443/`
e.g.
curl -v https://192.168.2.1:8443/

You should see something like 
 Trying 192.168.2.1...
 TCP_NODELAY set 
**Connected to 192.168.2.1 (192.168.2.1) port 8443 (#0)**

If that does not work, fix all network / routing / proxy / firewall related problems first. 

### 2. Test the datasource program / special agent

Execute the following command :

`cmk -D <E-Series Hostname in checkmk> | grep Program | cut -d ":" -f 3`
e.g.
`cmk -D eseries | grep Program | cut -d ":" -f 3`

The output is the so called "special agent" with its parameters that fetches the data of your netapp for checkmk. 
Copy that command and add the -vvv and --debug flags:

`/omd/sites/<your site name>/local/share/check_mk/agents/special/agent_netappeseries -u 'monitor' -s 'password' -vvv --debug 'ip-address'`

Now you can run that command and see, if data is being fetched.

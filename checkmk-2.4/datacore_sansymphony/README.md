Documentation
-------------

Preparations on the DataCore SANsymphony Servers
------------------------------------------------

If in doubt, talk to your DataCore Storage Consultant / Engineer.

1. Create a view-only user in DataCore SANsymphony

    - Create a local Windows user account on all servers in the ServerGroup with the same password
    - Add the user as a view-only account in DataCore SANsymphony
        - Click on the Ribbon "Users"
        - Register User
        - Enter the new user name
        - Choose the role "View"
        - Register
    - Save the users password in checkmks password store in setup - passwords

2. Rename your backend physical disks uniquely in the DataCore GUI

    If you don´t rename your physical disks uniquely, performance metrics will be mixed up in checkmk, as all disks of the same type will have the exact same name by default.
    Use meaningful names with the servername as a prefix like
        ssv1-sas-01
        ssv2-msa-ssd-001 
    or whatever makes sense in your environment.
    
    - On all SANsymphony servers in the SSV GUI:
        - Expand Pools - <Your Disk Pool>
        - Rename all the physical disks as described above
    
3. Set the REST API performance statistics caching interval to 180s

    If this is not configured, you will have empty values in the performance metrics

    https://docs.datacore.com/RESTSupport-WebHelp/RESTSupport-WebHelp/Getting_Performance_Statistcs.htm?Highlight=date
    
    On every server that is being monitored :
    - Remove the Read-Only flag from C:\Program Files\DataCore\Rest\Web.config
    - Edit C:\Program Files\DataCore\Rest\Web.config
    - Set the RequestExpirationTime to 180 : <add key="RequestExpirationTime" value="180"/>
    - save the file
    - Set the Read-Only flag to the file

4. If not yet configured - Enable TLS / https for SANsymphonys REST API

    - This should be automatically enabled on newer installations
    - https://docs.datacore.com/RESTSupport-WebHelp/RESTSupport-WebHelp/Changing_the_Hypertext_Transfer_Protocol.htm?Highlight=date


Installation in checkmk
-----------------------

This plugin is written with the new 2.3 check plugin API and will not work in older checkmk versions.

### 1. Install the checkmk extension package (MKP)
---------------------------
### 1.1 checkmk RAW Edition

- Download the latest checkmk mkp package netapp_eseries-version.mkp
- Copy the file to your checkmk server, e.g. to /tmp
- Make sure that the file is accessible by the "site user" of your monitoring site : `chown <site name> /tmp/datacore_sansymphony-<version>.mkp`
- Switch to your site user with `su - <your_site_name>`
- Change into the folder where you downloaded checkmk, e.g. `cd /tmp`
- Install the package with `mkp add ./datacore_sansymphony-<version>.mkp`
- Enable the package with `mkp enable datacore_sansymphony <version>`
- You can check if the package was successfully installed with the command `mkp list`
- After the installation of the mkp you can delete the downloaded package file

More Informations about installing mkps on the command line:
https://docs.checkmk.com/latest/en/mkps.html#_installation_of_an_mkp

### 1.2 checkmk Enterprise, Cloud, Free and Managed Services Edition

- Download the latest checkmk mkp package datacore_sansymphony-version.mkp
- Open the checkmk Webinterface, select "Setup" - "Extension packages"
- If the entry "Extension packages" is not shown, click on "show more" on the top right of the setup menu
- Select "Upload package"
- Select the downloaded file and "Upload & install"

More Informations about installing mkps in the checkmk webinterface:
https://docs.checkmk.com/latest/en/mkps.html#wato


### 3. Add the SANsymphony hosts to checkmk
---------------------------

This plugin connects to DataCore SANsymphony via the Rest API and fetches all SANsymphony related informations. The installation of the checkmk agent is not necessary for pure sansymphony monitoring, if you want further OS related monitoring (e.g. CPU, RAM, Filesystems, Event Logs) you can additionally install the checkmk agent on the sansymphony servers.

- Add the hosts in setup
- Set "Checkmk agent / API integrations" to 
    - "API integrations if configured, else checkmk agent" if you only want to monitor the servers via the REST API
    - "API integrations if configured and checkmk agent" if you plan to install the checkmk agent on the servers

I would recommend to create separate hosts to monitor the server hardware through the management boards (ideally with the redfish plugin)

### 4. Add a password entry for the read only user to the password store
---------------------------

- Setup / General / Passwords
- Add Password
- Enter a unique id, title and the password itself

### 5. Configure the ruleset "DataCore SANsymphony via REST API"
---------------------------

Enter the following informations

- Username
- Password from Password store
- If the Sansymphony server name differs from its name in checkmk, enter the servername as shown in the SSV GUI
- Configure the advanced settings if necessary

### 6. Discover the hosts
---------------------------

- Select the sansymphony host in setup
- Save & run service discovery
- Activate the changes with the orange icon on the top right
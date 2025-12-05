Documentation
-------------

Preparations on the DataCore SANsymphony Servers
------------------------------------------------

If you are uncertain, consult your DataCore Storage Consultant or Engineer.

1. Create a view-only user in DataCore SANsymphony

    - Create a local Windows user account on all servers in the ServerGroup with the same password
    - Add the user as a view-only account in DataCore SANsymphony
        - Click on the Ribbon "Users"
        - Register User
        - Enter the new user name
        - Choose the role "View"
        - Register
    - Save the user's password in CheckMK's password store (Setup → Passwords)

2. Rename your backend physical disks uniquely in the DataCore GUI

    If you do not rename your physical disks uniquely, performance metrics will be mixed up in CheckMK, as all disks of the same type will have the exact same name by default.
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
    
    On every server that is being monitored:
    - Remove the Read-Only flag from C:\Program Files\DataCore\Rest\Web.config
    - Edit C:\Program Files\DataCore\Rest\Web.config
    - Set the RequestExpirationTime to 180 : <add key="RequestExpirationTime" value="180"/>
    - save the file
    - Set the Read-Only flag on the file

    **Note:** This file is reset during SANsymphony updates. Repeat these steps after each update.

4. If not yet configured - Enable TLS / https for SANsymphonys REST API

    - This should be automatically enabled on newer installations
    - https://docs.datacore.com/RESTSupport-WebHelp/RESTSupport-WebHelp/Changing_the_Hypertext_Transfer_Protocol.htm?Highlight=date


Installation in CheckMK
-----------------------

This plugin is written with the new CheckMK 2.3 check plugin API and will not work in older CheckMK versions.

### 1. Install the CheckMK extension package (MKP)

#### 1.1 CheckMK RAW Edition

- Download the latest MKP package `datacore_sansymphony-<version>.mkp`
- Copy the file to your CheckMK server, e.g., to `/tmp`
- Make sure that the file is accessible by the site user of your monitoring site: `chown <site_name> /tmp/datacore_sansymphony-<version>.mkp`
- Switch to your site user with `su - <your_site_name>`
- Change into the folder where you downloaded the package, e.g., `cd /tmp`
- Install the package with `mkp add ./datacore_sansymphony-<version>.mkp`
- Enable the package with `mkp enable datacore_sansymphony <version>`
- Verify the installation with `mkp list`
- After installation, you can delete the downloaded package file

For more information about installing MKPs on the command line, see:
https://docs.checkmk.com/latest/en/mkps.html#_installation_of_an_mkp

#### 1.2 CheckMK Enterprise, Cloud, Free and Managed Services Edition

- Download the latest MKP package `datacore_sansymphony-<version>.mkp`
- Open the CheckMK web interface and navigate to Setup → Extension packages
- If "Extension packages" is not visible, click "show more" in the top right of the Setup menu
- Select "Upload package"
- Select the downloaded file and click "Upload & install"

For more information about installing MKPs in the CheckMK web interface, see:
https://docs.checkmk.com/latest/en/mkps.html#wato


### 2. Add the SANsymphony hosts to CheckMK

This plugin connects to DataCore SANsymphony via the REST API and fetches all SANsymphony-related information.

Installing the CheckMK agent is not required for SANsymphony monitoring. However, if you want additional OS-level monitoring (e.g., CPU, RAM, filesystems, event logs), you can install the CheckMK agent on the SANsymphony servers.

- Add the hosts in Setup
- Set "CheckMK agent / API integrations" to:
    - "API integrations if configured, else CheckMK agent" if you only want to monitor the servers via the REST API
    - "API integrations if configured and CheckMK agent" if you plan to install the CheckMK agent on the servers

It is recommended to create separate hosts for monitoring server hardware through management boards (ideally using the Redfish plugin).

### 3. Add a password entry for the read-only user to the password store

- Navigate to Setup → General → Passwords
- Click "Add Password"
- Enter a unique ID, title, and the password

### 4. Configure the ruleset "DataCore SANsymphony via REST API"

Enter the following information:

- Username
- Password from the password store
- If the SANsymphony server name differs from its name in CheckMK, enter the server name as shown in the SSV GUI
- Configure advanced settings if necessary

### 5. Discover the hosts

- Select the SANsymphony host in Setup
- Click "Save & run service discovery"
- Activate the changes using the orange icon in the top right
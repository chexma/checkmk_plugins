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
#######################

1. Install the MKP file

    1. Enterprise / Cloud Edition

    2. Raw Edition

. Add the sansymphony hosts to checkmk

. Configure the ruleset "DataCore SANsymphony via REST API"

    - Username
    - Password from Password store
    - 
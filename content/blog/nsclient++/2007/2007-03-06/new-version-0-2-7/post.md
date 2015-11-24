Title: New version: 0.2.7
Author: mickem
Status: published

New version out so let me know how it work, nothing major new but some
bug fixes and some minor improvements such as eventlog-check has a
better syntax, support for net-masks in host lists, option to add a
directory (and all files in it) as scripts. And hopefully the several
times already fixed broken passwords are now finally fixed :) Issues
resolved: \#16, \#17, \#22, \#26, \#29, \#32, \#33, \#34, \#35, \#38,
\#11, \#39 Changelog highlights

     * Fixed -v FILEAGE check_nt (NSClient) check. + Added script_dir option to NRPE scetion as well as some sample scripts in the scripts/ subdirectory. The script_dir will use all files in this directory as scripts for NRPE + Added possibility to check many memory checks in one go, just stack type options. type=paged type=physical etc... + Added netmask support to allowed_hosts (try with 192.168.0.1/24 and such) + Added configuration option for suppressing performance datat to the NRPE section. Set performance_data=0 to stop sendoing performancedata to nagios + New (better?) (simpler?) eventlog checking + Added option to most commands (ignore-perf-data) to suppres performance data + Added option CheckAll for checking all auto-start services to checkServiceState. Also an exclude= to exclude checking that. * Fixed "broken password check" (again) in NSClient listener (this time it is correct! :) 

Title: New "nightly" build up
Author: mickem
Status: published

\*\*UPDATED\*\* Added a new nightly build that should work, please try
it out and get back to me, this will be become 0.2.7 in the near future.
Resolved: \#16, \#17, \#22, \#26, \#29, \#32, \#33, \#34, \#35, \#38,
\#11, \#39 If nothing else pops up I will release 0.2.7 tomorrow...
Changelog

     2006-03-05 MickeM * Fixed -v FILEAGE check_nt (NSClient) check. * Added licence agreement header to all files 2006-03-04 MickeM + Added script_dir option to NRPE scetion as well as some sample scripts in the scripts/ subdirectory. The script_dir will use all files in this directory as scripts for NRPE + Added japanese counters to counters.defs from patch (thanx!!!) 2006-02-25 MickeM + Added possibility to check many memory checks in one go, just stack type options. type=paged type=physical etc... * Fixed a performance check bug in the last nightly. * Fixed a potential crash when a maleformed check-file-age command was issued. + Added support for more then and NSClient command + Added netmask support to allowed_hosts (try with 192.168.0.1/24 and such) 2006-02-22 MickeM + Added debug output to see if the socket is bound and/or has shutdown. * Fixed a potential bug in the threadmanager. + Added configuration option for suppressing performance datat to the NRPE section. Set performance_data=0 to stop sendoing performancedata to nagios + New (better?) (simpler?) eventlog checking + Added option to most commands (ignore-perf-data) to suppres performance data + Added option CheckAll for checking all auto-start services to checkServiceState. Also an exclude= to exclude checking that. * Fixed return syntax for PROCSTATE nsclient 2006-02-21 MickeM * Fixed "broken password check" (again) in NSClient listener (this time it is correct! :) 

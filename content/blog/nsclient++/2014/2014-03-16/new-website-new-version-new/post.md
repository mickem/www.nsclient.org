Title: New Website, new version, new…
Author: mickem
Tags: 0.4.2, release
Status: published

Greetings all!

New big tidings. Not just the long overdue release of 0.4.2 but also a
brand new web site.

I have been planning a new website for some time but haven't gotten
around to it until now. Hopefully the new site will be a bit simpler to
navigate and more importantly simpler for me to communicate with you.
The focus now have been on creating a base site which has the
information part of NSClient++ and put all the documentation in the
documentation site. In the near future I will migrate the forum over to
a WordPress version and see what to do about the tickets. They might go
to github or something along those lines. But that has yet to be
decided.

**Full changelog is here:**

    2014-03-10 MickeM
     * Fixed server restarting listeners on errors

    2014-03-08 MickeM
     * Added total object to check_files
     * Fixed registry issues

    2014-03-06 MickeM
     * Fixed performance config order
     * Fixed external script alias and support for help-csv

    2014-03-05 MickeM
     * Fixed crash dump issue
     * Fixed memory leak in NSCA

    2014-03-04 MickeM
     * Fixed issue with CheckTaskSched and status #702
     * Improved rendering of status #702
     * Added some debug logging to eventlog to help diagnose issues
     * Fixed default crash dump folder config issue

    2014-02-23 MickeM
     * Changed so uniq is default for eventlog checks (if no arguments are given)
     * Fixed drives so they are more sensible
     * Added drive_or_id and drive_or_name to configure the default "id" of drives.
     * Fixed so legacy MaxWarn/MinWarn/MaxCrit/MinCrit are treated like >= and <= (which is the original behaviour)
     * Changed so default "help" if invalid syntax is the short version.
     * Removed erronouse logging when shutting down sockets
     * Tweaked console output a bit
     * Fixed check_uptime overflow issue

    2014-01-25 MickeM
     * Fixed FILEAGE check_nt command #480, #636, #642, #39 (and others)
     * Fixed delayed start issue in check_service #681
     * Fixed not regexp issue #651
     * Fixed default service name
     * Fixed issue with scan-range #683
     * Fixed uptime performance alias (and added unit s) #688
     * Fixed issue with CkeckCPU show-all: #687
     * Fixed issue with check_ping.bat #635
     * Fixed documentation for nsca hostname #690
     * Fixed validation issues with lists #605
     * Fixed so external script errors are reported againast the alias not the command #677

    2014-01-04 MickeM
     * Numerous bugfixes and compatiblity fixes
     * Gone over all unit tests to make sure they run

    2013-12-23 MickeM
     * Added support for unique
     * Fixed unique and debug flags in CheckEventLog

    2013-12-20 MickeM
     * Fixed issue with check_nt and units beeing reounded to nearest bg, mg, kb, etc)
     * Added support for configuring performance data

    2013-12-18 MickeM
     * Fixed source in new eventlog
     * Added truncate-message option to check eventlog to truncate the message
     * Added filtering of cr,lf in eventlog messages
     * Fixed performance data naming in event log

    2013-12-10 MickeM
     * renamed "full config" sample to reduce confusion.
     * Fixed numerous issues with check_files and CheckFiles (now all CheckFiles unit test work as expected)

    2013-12-09 MickeM
     * Fixed a crash in handling ${status} in some filters.
     * Added check_nrpe to the installer
     * Changed symbol paths (in zip) now correspond to what breakpad expects

    2013-12-05 MickeM - RC3
     * Added suport for instances (new keyword instances) to check_pdh
     * Fixed more compatiblity issues

    2013-12-04 MickeM
     * Added check_cpu_ex.lua script to return top consumers for check_cpu command.
     * Harmonized the compatiblity layer so all commands "work the same"

    2013-12-03 MickeM
     * Added new command: filter_perf to filter the returned performance data
     * Fixed some issues (API changes) in Lua script module

    2013-11-29 MickeM
     * Fixed issue with logger

    2013-11-28 MickeM
     * Added %() for all expressions to make esacping in nagios simpler.
     * Fixed crash in check_nscp
     * CheckDriveSize (compatiblity) fixed support for multiple bounds will only use "one of them" though.
     * Fixed some regression issues for check_nt (disk, memory uptime, services)
     * Added $ARGS$ to CheckExternalScript to add scripts with variable argument lists
     * Added $ARGS"$ to CheckExternalScript to add scripts with qouted variable argument lists

    2013-11-27 MickeM
     * Fixed _user arguments for check:drivesize (which can be used for drives with qouta)

    2013-11-26 MickeM
     * Improved compatiblity for CheckDriveSize
     * Added total (option) to check_drive to get/check the total size of all (matching) drives
     * Fixed bounds calculation for check_drivesize
     * Fixed issue with the show-all flag beeing on by default.
     * Fixed issue with converting to byte units for very large/small numbers

    2013-11-22 MickeM
     * Updated documentation
     * Added sample for most commands
     * Fixed syntax issues with online help
     * Fixed so PDF documentation builds correctly
     * Fixed check_uptime to be more sensible (i.e. uptime is just a value not a strange date thingy)
     * Added compatiblity for CheckTaskSched

    2013-11-21 MickeM
     * Fixed some check_drivesize perfdata issues
     * Fixed check_drivesize type filter keyword
     * Fixed CheckDriveSize compatiblity issues

    2013-11-20 MickeM
     * Added support for setting source in schedules to override hostname
     * Fixed real-time eventlog defaults

    2013-11-19 MickeM
     * Fixed links in documentation
     * Fixed bugs in documentation generator (missing sections)
     * Fixed hostnames for NSCA/NRDP

    2013-11-17 MickeM
     * Fixed CheckEventLog compatiblity

    2013-11-08 MickeM
     * Improved check_nt compatiblity
     * Added back lines as alias for list in top syntaxes.

    2013-11-08 MickeM
     * Finally fixed broken unit test on "linux" (Which was a case error as always, damn you ntfs!!)
     * Fixed some dependencies in the vagrant puppet conf
     * Added oracle linux vagrant profile (but doesn't seem to work :(
     * Added support for external script (Linux side)
     WARNING: No timeout handling (yet)
     * Added test cases for external script to ctest

    2013-11-07 MickeM
     * Fixed issue with NSCA hostname (NSCAClient load).
     * Fixed check_nt commands
     * Added vagrant files to load-up machines and build NSClient++ (ubuntu)

    2013-11-03 MickeM
     * Fixed so lua script are now loaded with a missing .lua extension
     * Fixed Lua some remaining invalid lua functio issues.
     * Fixed unit test for Lua scripts.
     * Fixed forwarding (for clients)
     * Fixed test_nrpe (lua)

    2013-10-29 MickeM
     * Added json_sprit as a submodule to see if this works better.
     * Changed so json_sprit now builds using their own cmake file which means it should hopefully be better ready for future versions.

    2013-10-28 MickeM
     * Compatiblity layer added for most "old" checks.
     The way this works is that CheckCpu is the old check and check_cpu is the new.
     * Fixed a lot of check related bugs
     * Added a bunch of check related options such as exclude and so on and so forth.

    2013-10-20 MickeM
     * Added real-time checks for cpu and memory (CheckSystem)
     * Refactored client handling a bit to make it simpler to create stand alone clients.
     * Added check_nrpe client

    2013-10-17 MickeM
     * A lot of Linux fixes
     * Refactored real-time stuff to make it easier to add in new places
     * NSCA/NRPE fixes

    2013-10-10 MickeM
     * Added back CheckWMI based on new filters.
     * Fixed issues with building on Linux
     * Added support for WMI and float types (type 4 and 5)

    2013-09-24 MickeM
     * Fixed issue with performance data and byte based units
     * Added total to check_pagefile

    2013-09-23 MickeM
     * Removed page (since it often is wrong)
     * Added check_pagefile (to check pagefile usage)
     * removed nobp (wince it was for NT4 and we dont support nt4)
     * Removed debug symbols (since breakpad symbols work)

    2013-09-19 MickeM
     * Fixed issue with skipping registry
     * Added page (commited - physical) memory metric

    2013-09-17 MickeM
     * Added support for new eventlog API.
     This means NSClient++ can FINALLY! check all eventlogs on windows 2008 and windows 2012!

    2013-09-16 MickeM
     * Fixed NRPE issue

    2013-09-09 MickeM
     * Fixed check_multi
     * added new options to check_multi (suffic, prefix and separator) to better control the output
     * starting services (auto-start) is now a warning state.

    2013-09-08 MickeM
     * Brand new filters
     * Modernised check_cpu
     * Modernised check_process
     * Modernised check_service
     * Modernised check_uptime
     * Modernised check_tasksched
     * Merged CheckTaskSched1 and CheckTaskSched2 into CheckTaskSched
     * Added check_os_version

    2013-05-05 MickeM
     * Fixed a bug in the check_logfile which made filtering bail-out after the first hit.
     * Added default column-split as \t

    2013-04-30 MickeM
     * Fixed issue with negative performance data
     * Added unit test for arguments and external script
     * Fixet truncation issue with performance data (#624)

    2013-04-27 MickeM
     * Fixed bug added in build 95 regarding allowing nasty characters

    2013-04-24 MickeM
     * Added auto-uc to get hostname as upper case

    2013-04-23 MickeM
     * Added encoding option to external scripts
     * Added encoding option to NSCAClient
     * Added NSCPDOTNET.dll for making dot-net plugins

    2013-04-22 MickeM
     * Fixed an issue with % in warn and crit thresholds for CheckCPU

    2013-04-21 MickeM
     * Fixed issue with eventlog reset (will not rescan from the beginning if an error is encountered)

    2013-04-16 MickeM
     * re-added check_nt FILEAGE option.

    2013-04-13 MickeM
     * Fixed issue with binding to multiple interfaces (ie. machines with both ipv6 and ipv4 addresses).
     * Fixed some missing documentation from core settings keys such as /settings/log and /includes.
     * Added debug message warning about having $ARG??$ in external scripts wehn allowe arguments is false.
     * Removed need to escape and qoute commands for external scripts (command line will now be used as-is)
     * Fixed qouting issues with external scripts

    2013-01-21 MickeM
     * Fixed two include files issues

    2013-01-19 MickeM
     * Fixed Wix 3.7 and added wix to dependencies


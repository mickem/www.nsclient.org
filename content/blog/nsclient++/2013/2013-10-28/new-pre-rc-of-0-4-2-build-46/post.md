Title: New pre-RC of 0.4.2 (build 46)
Author: mickem
Tags: 0.4.2, release-candidate
Status: published

Hello, The first pre-RC build of 0.4.2 is out (**build 0.4.2.46**)\
 The main new feature is the CompatiblityLayer which has been added
which means "most" old check should work. Please note that this is
something I hope you will help out with so if your old checks don't work
please get back to me and I will try to add support for them!

Apart from this there is a bunch of new options to make many checks
simpler to use as well as bugfixes and enhancements all over. I will
start running some internal tests on this build now as well but please
do try to help out as well! If all goes well the first RC will be out
later this week!

**Changelog:**

     2013-10-28 MickeM
     * Compatiblity layer added for most "old" checks. The way this works is that CheckCpu is the old check and check_cpu is the new.
     * Fixed a lot of check related bugs
     * Added a bunch of check related options such as exclude and so on and so forth. 
    2013-10-20 MickeM
     * Added real-time checks for cpu and memory (CheckSystem)
     * Refactored client handling a bit to make it simpler to create stand alone clients.
     * Added check_nrpe client 
    2013-10-17 MickeM
     * A lot of Linux fixes
     * Refactored real-time stuff to make it easier to add in new places
     * NSCA/NRPE fixes 2013-10-10 MickeM
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

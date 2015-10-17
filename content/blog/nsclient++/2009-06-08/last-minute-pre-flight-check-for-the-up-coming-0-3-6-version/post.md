Title: Last minute pre-flight check for the up-coming 0.3.6 version
Author: mickem
Tags: release-candidate
Status: published

Not much news in this build which contains a bunch of bug-fixes as well
as a compleate version of the new installer. \* CheckFileAge (was
broken) \* NSCA config option time\_delay was off by 1000. \* Eventlog
monitoring with descriptions flag was crashing on x64. \* CheckProc
works better on x64 \* New installer is "finalized" The RC is called X
this time as I did not want to rename all the others. If no one reports
in bugs this will become 0.3.6 release in 24 hours or so. Full change
log:

     2009-06-07 MickeM * Fixed issue with CheckFileAge incorrectly working in recursive mode. * Finalized the installer 2009-05-22 MickeM * Fixed time_delay option in NSCA config (now uses the correct base was 1000 times to large before) 2009-05-21 MickeM * Fixed issue with eventlog parsing and 64 bit machines (descriptions option) * Fixed issue with "modern windows" and installing the service (should not have the correct privlaiges) 2009-05-17 MickeM * Changed default buffer size for process enumeration (64K now instead of 1K should I hope work better on 64bit OS:es) 2009-05-10 MickeM + Added write support for modules to installer 

// Michael Medin

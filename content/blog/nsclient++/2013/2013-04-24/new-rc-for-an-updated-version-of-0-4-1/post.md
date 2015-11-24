Title: New RC for an updated version of 0.4.1
Author: mickem
Tags: 0.4.1, release-candidate
Status: published

A new update for 0.4.1 is available as a release candidate now. If no
one reports any major bug this build will be released as an update to
0.4.1 in a week or so. So please everyone help out and make sure there
are no major bugs and/or issues. This contains some bugfixes as well as
a few enhancements some of the highlights are: \* Encoding support (for
External scripts as well as NSCA) \* Eventlog reset issues for realtime
monitoring \* Readded the check\_nt -v FILEAGE check \* Qouting of
command lines now works \* No works with both an ipv6 and ipv4 interface
// Michael Medin The full changelog is here:

     2013-04-23 MickeM * Added encoding option to external scripts * Added encoding option to NSCAClient * Added NSCPDOTNET.dll for making dot-net plugins 2013-04-22 MickeM * Fixed an issue with % in warn and crit thresholds for CheckCPU 2013-04-21 MickeM * Fixed issue with eventlog reset (will not rescan from the beginning if an error is encountered) 2013-04-16 MickeM * re-added check_nt FILEAGE option. 2013-04-13 MickeM * Fixed issue with binding to multiple interfaces (ie. machines with both ipv6 and ipv4 addresses). * Fixed some missing documentation from core settings keys such as /settings/log and /includes. * Added debug message warning about having $ARG??$ in external scripts wehn allowe arguments is false. * Removed need to escape and qoute commands for external scripts (command line will now be used as-is) * Fixed qouting issues with external scripts 2013-01-21 MickeM * Fixed two include files issues 2013-01-19 MickeM * Fixed Wix 3.7 and added wix to dependencies 

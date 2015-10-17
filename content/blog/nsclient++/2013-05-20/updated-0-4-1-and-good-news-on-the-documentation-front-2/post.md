Title: Updated 0.4.1 and good news on the documentation front!
Author: mickem
Tags: docs, release
Status: published

A new version of 0.4.1 is now available fixing a number of issues as
well as some minor enhancements. The main enhancements are: \* Encoding
support. Encodings are now supported via NSCA/NRPE as well as external
scripts meaning you should be able to resolve any encoding issues. \*
NSCA hostname can now be made upper or lowercase (using auto schemes)
For full details read the full change log at the end.
'''Documentation:''' I have for the first time ever started to work more
proactively on documentation. This means I will soon be shipping proper
documentation starting with 0.4.2. It also means the wiki as
documentation will be abandoned instead a new documentation only site
will be launched. The documentation system is sphinx which is the one
python use so hopefully it will turn out as nice documentation. A
preview of the documentation is deployed here (please understand that is
is all very temporary) so feel free to let me know what you think:
http://www.nsclient.org/trac/tmp/ once it is improved and I have
resolved the auto documentation issues it will be moved over to
http://docs.nsclient.org '''Full changelog of 0.4.2.101:'''

     2013-05-18 MickeM * Fixed issue with NSCA hostname * Fixed "ok ping" date handling in real-time check_log_file 2013-05-05 MickeM * Fixed a bug in the check_logfile which made filtering bail-out after the first hit. * Added default column-split as t 2013-04-30 MickeM * Fixed issue with negative performance data * Added unit test for arguments and external script * Fixed truncation issue with performance data (#624) 2013-04-27 MickeM * Fixed bug added in build 95 regarding allowing nasty characters 2013-04-24 MickeM * Added auto-uc to get hostname as upper case 2013-04-23 MickeM * Added encoding option to external scripts * Added encoding option to NSCAClient * Added NSCPDOTNET.dll for making dot-net plugins 2013-04-22 MickeM * Fixed an issue with % in warn and crit thresholds for CheckCPU 2013-04-21 MickeM * Fixed issue with eventlog reset (will not rescan from the beginning if an error is encountered) 2013-04-16 MickeM * re-added check_nt FILEAGE option. 2013-04-13 MickeM * Fixed issue with binding to multiple interfaces (ie. machines with both ipv6 and ipv4 addresses). * Fixed some missing documentation from core settings keys such as /settings/log and /includes. * Added debug message warning about having $ARG??$ in external scripts wehn allowe arguments is false. * Removed need to escape and qoute commands for external scripts (command line will now be used as-is) * Fixed qouting issues with external scripts 2013-01-21 MickeM * Fixed two include files issues 2013-01-19 MickeM * Fixed Wix 3.7 and added wix to dependencies 

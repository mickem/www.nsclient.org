Title: New 0.3.8 Nightly build out!
Author: mickem
Tags: 0.3.8, nightly
Status: published

Again more improvements and changes to the disk related checks.
Highlights are: \* Better performance data for CheckDrive (now always
shows absolute sizes) so you can plot better graphs. \* Volume support
for CheckDriveSize (CheckAll=volumes) \* User support in syntax for
CheckEventLog \* Support for "future dates" '''Now is a very good time
to submit all feature requests for disk related checks as I am working
over those parts.''' Full changlog

     2009-12-31 MickeM * Fixed CheckFile* time handling so it is "signed" This means you can check for "future dates" as well as future dates works correctly: Like so: CheckFile2 debug path=D:tmpdates filter+creation=>30m MaxWarn=1 MaxCrit=1 "syntax=%filename%: %creation%" CRITICAL:past.txt: Thursday, December 31, 2009 08:47:30, found files: 1 > critical|'found files'=1;1;1; CheckFile2 debug path=D:tmpdates filter+creation=<-30m MaxWarn=1 MaxCrit=1 "syntax=%filename%: %creation%" CRITICAL:future.txt: C: Thursday, December 31, 2009 12:47:11, found files: 1 > critical|'found files'=1;1;1; + Added volume support for CheckDriveSize (CHeckAll) like so: Like so: CheckDriveSize MinWarn=50% MinCrit=25% CheckAll=volumes FilterType=FIXED FilterType=REMOTE + Added %user% to syntax to print user who generated message. Like so: CheckEventLog file=application file=system filter=new filter=out MaxWarn=1 MaxCrit=1 filter-generated=>2w filter-severity==success filter-severity==informational truncate=1023 unique descriptions "syntax=%user% (%count%)" CRITICAL: (1), (2), NT INSTANSSYSTEM (3), NT INSTANSSYSTEM (3), NT INSTANSSYSTEM (3), missing (3), missing (5), (4), missing (2), missing (2), missing (2), missing (2), (1), eventlog: 33 > critical|'eventlog'=33;1;1; 2009-12-21 MickeM ! BREAKING CHANGE! ! New perfoamcen data syntax for ALL % checks Alias is ' %' and it also has the "full" non % data as '' Like so: CheckDriveSize CheckAll MaxWarnUsed=80% MaxCritUsed=90% CRITICAL:CRITICAL: C:: Total: 146G - Used: 140G (95%) - Free: 6.31G (5%) > critical, D:: Total: 152G - Used: 148G (97%) - Free: 3.59G (3%) > critical|'C: %'=95%;80;90; 'C:'=140.17G;117.18;131.83;0;146.48; 'D: %'=97%;80;90; 'D:'=147.93G;121.21;136.3;0;151.52; CheckDriveSize CheckAll MaxWarnFree=20% MaxCritFree=10% OK:OK: All drives within bounds.|'C: %'=5%;20;10; 'C:'=140.17G;29.29;14.64;0;146.48; 'D: %'=3%;20;10; 'D:'=147.93G;30.30;15.15;0;151.52; CheckDriveSize CheckAll MaxWarnUsed=100G MaxCritUsed=150G WARNING:WARNING: C:: Total: 146G - Used: 140G (95%) - Free: 6.31G (5%) > warning, D:: Total: 152G - Used: 148G (97%) - Free: 3.59G (3%) > warning|'C: %'=95%;32;4294967294; 'C:'=140.17G;100;150;0;146.48; 'D: %'=97%;35;2; 'D:'=147.93G;100;150;0;151.52; CheckDriveSize CheckAll MaxWarnFree=20G MaxCritFree=10G OK:OK: All drives within bounds.|'C: %'=5%;87;94; 'C:'=140.17G;20;10;0;146.48; 'D: %'=3%;87;94; 'D:'=147.93G;20;10;0;151.52; 

// Michael Medin

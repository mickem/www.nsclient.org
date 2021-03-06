Title: 0.3.8 Released!
Author: mickem
Status: published

Hello google bot! (and some happy weeks even the yahoo bot). I have just
released 0.3.8 version. It has a lot of new features and, I am
especially, proud of the new event log filters. I will try to see if I
can propagate it out to sourceforge and nagios forge during the weekend
unfortunately I did not have time this morning... For those who has not
seen the eventlog filter I recommend reading up on the quick guide i
wrote on the \[wiki:CheckEventLog/CheckEventLog\] page. It has a fairly
good getting started guide I hope. But a quick note is that the new
default filter is:

     generated > -2d AND severity NOT IN ('success', 'informational') 

Which I believe is a lot more readable the before. Other news are many
minor changes and fixes in the file7disk related checks as well as index
in CheckCounter to allow handling multiple languages and locales. The
changelog grouped by module can be found here:

* New commands 
** CheckSingleFile 
   to check spects of a single file use like so: CheckSingleFile file=d:nrpe_512.pem warn=>100 check=line-count warn=>100 crit=>170 check=size 
** CheckSingleRegEntry 
   CheckSingleRegEntry path=HKEY_LOCAL_MACHINESYSTEMCurrentControlSetserviceseventlogApplicationMaxSize "syntax=%path%: %int%" warn==20971520 crit==20971520 check=int ShowAll=long Scripts 
* Cleaned up scripts folder 
* Added new "NagiosPlugin library" from op5 
* Added check_no_rdp.vbs (Checks that no RDP connection is online) 
* Added check_battery.vbs which checks batterys via WMI 
* Added check_printer.vbs to check printers via WMI CheckExternalScript 
* Added new "script templating" thing to simplify adding scripts: [Wrapped Scripts] test=check_test.ps1 ; (will use correct template for running ps1 commands) 
* Fixed erroneous error message "Failed to peek buffer" NSCA 
* Added obfuscated_password to NSCA section 
* Added so "global" ([Settings] password=...) passwords are read from the NSCA module CheckEventLog 
* Brand new filter syntax based on SQL where clauses Avalible operators are: =, !=, >, <, >=, <=, eq, ne, gt, lt, ge, le, OR, AND, like, IN, NOT IN CheckCounter 
* Added new index option to CheckCounter to allow looking up index and thus you can use the same checks on multiple locales and also use characters not present in "NRPE charset) CheckCounter index "Counter=1450(_Total)1458" ShowAll MaxWarn=500 MaxCrit=1000 nsclient++  -noboot CheckSystem pdhlookup Utskrifter 
* Optional new "safe" PDH subsystem (slower, but possibly safer) pdh_subsystem=thread-safe 
* Added checks for missing counters to CheckCounter CheckDriveSize 
* Added volume support for CheckDriveSize (CHeckAll) like so: CheckDriveSize MinWarn=50% MinCrit=25% CheckAll=volumes FilterType=FIXED FilterType=REMOTE 
* Changed "missing" disks are now a critical error and not unknown 
* Improved CheckDriveSize bad FilterType error message 
** Added option to return error messages to the client [CheckDisk] show_errors=1 (defauilt is off 0) CheckFile2 
** Dates are signed (means you can use neagitve dates to check the future) CheckFile2 debug path=D:tmpdates filter+creation=< -30m MaxWarn=1 MaxCrit=1 "syntax=%filename%: %creation%" CRITICAL:future.txt: C: Thursday, December 31, 2009 12:47:11, found files: 1 > critical|'found files'=1;1;1; 
** Added checks for missing path and missing filter on CheckFile2 thus 
** Fixed so files locked for reading can be checked (basic checks) 
** Improved speed of file chyecking (does not check file data twice) 
* Changed so missing files and such generate an error 
* Fixed major issue with date matching in CheckFile* which was not working at all. 
* Exe file version checks: CheckFile2 path=D:tmp pattern=*.exe filter+version=!=6.0.2900.5512 "syntax=%filename%: %version%" MaxWarn=1 
* Line count check: CheckFile2 path=D:tmp pattern=*.txt filter+line -count=ne:3 "syntax=%filename%: %line -count%" MaxWarn=1 
* Added ignore-errors to "ignore" any filesystem related errors (NOTICE this is probably not what you want) 
* Added master-syntax to CheckFile2 to change the overall message like so: %list%, %files%, %matches% CheckFile2 MinWarn=10 MinCrit=10 path=D:WINDOWSsystem32 filter+size=gt:0 truncate=10 ignore-errors "master-syntax=%matches%/%files%" 
* Added %user% to syntax to print user who generated message CheckEventLog file=application file=system filter=new filter=out MaxWarn=1 MaxCrit=1 filter-generated=>2w filter-severity==success filter-severity==informational truncate=1023 unique descriptions "syntax=%user% (%count%)" CRITICAL: (1), (2), NT INSTANSSYSTEM (3), NT INSTANSSYSTEM (3), NT INSTANSSYSTEM (3), missing (3), missing (5), (4), missing (2), missing (2), missing (2), missing (2), (1), eventlog: 33 > critical|'eventlog'=33;1;1; Generic: 
* Added != to all string comparisons 
* Changes syntax of performance counters: Alias is ' %' and it also has the "full" non % data as '' CheckDriveSize CheckAll MaxWarnUsed=80% MaxCritUsed=90% CRITICAL:CRITICAL: C:: Total: 146G 
* Added warning message ewhen numerical filters evaluate to zero (and are not 0) 
* added a new "option" in conjunction with -c you can now do -m to specify the module to load. nsclient++ -m CheckDisk.dll -c CheckDriveSize MaxWarn=100 CheckAll 

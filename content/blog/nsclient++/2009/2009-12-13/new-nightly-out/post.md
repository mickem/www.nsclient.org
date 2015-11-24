Title: New nightly out!
Author: mickem
Tags: nightly
Status: published

Mainly disk and file related additions: \* New command: CheckSingleFile
\* A few new options for CheckFile2 Full changelog here

     2009-12-13 MickeM + Added new command: CheckSingleFile to check aspects of a single file use like so: CheckSingleFile file=d:nrpe_512.pem warn=>100 check=line-count warn=>100 crit=>170 check=size + Added option debug to CheckFile2 to enable printing of debug information + Added ignore-errors to "ignore" any filesystem related errors (NOTICE this is probably not what you want) + Added master-syntax to CheckFile2 to change the overall message like so: It takes three options (and char data): * %list% A list of all "files" (syntax controls this) * %files% number of files * %matches% number of files matched CheckFile2 MinWarn=10 MinCrit=10 path=D:WINDOWSsystem32 filter+size=gt:0 truncate=10 ignore-errors "master-syntax=%matches%/%files%" OK:7177/7...|'found files'=7177;10;10; 2009-12-06 MickeM + Added != to all string filters + Sorted out the alias handling it is now wither what you specify or "files found" (this makes performance data work) + Added version to CheckFile2 CheckFile2 path=D:tmp pattern=*.exe filter+version=!=1.0 "syntax=%filename%: %version%" MaxWarn=1 CheckFile2 path=D:tmp pattern=*.exe filter+version=!=6.0.2900.5512 "syntax=%filename%: %version%" MaxWarn=1 + Added line count to CheckFile2 to count lines CheckFile2 path=D:tmp pattern=*.txt filter+line-count=!=2 "syntax=%filename%: %line-count%" MaxWarn=1 CheckFile2 path=D:tmp pattern=*.txt filter+line-count=ne:3 "syntax=%filename%: %line-count%" MaxWarn=1 

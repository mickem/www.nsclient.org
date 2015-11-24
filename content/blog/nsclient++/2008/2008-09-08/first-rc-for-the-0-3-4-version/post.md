Title: First RC for the 0.3.4 version!
Author: mickem
Status: published

Well, time for the first RC for the 0.3.4 upcoming release. This issue
has (since the last nightly a few days ago) a few bug fixes and some
minor additions. The plan is still to try to get 0.3.4 out next week
(unless something big pops up) I consider this release pretty stable so
feel free to start trying it out.

     2008-09-08 MickeM * Fixed issue in windows 2008 with system tray (shared_session). * Fixed installer issue (should run (i hope) service installer on install now on 64 bit os) * Fixed issue with unloading plugins and log (causing "timeouts" when exiting some times) 2008-09-07 MickeM + Added sample powershell script as well as a workaround for making them run. * Fixed an issue making powershell scripts (and possibly others) not timeout properly. + Added upgrade support to the installer (still need to add support for keeping .ini file so be ware) 2008-09-06 MickeM * Improved error reporting in the eventlogchecker * *BREAKING CHANGE* filter=new is now the default so unless you use the new filtering you need to specify filter=old instead! I Recommend everyone to stop using the "old" filtering. 

// MickeM

Title: Second 0.4.0 beta out!
Author: mickem
Tags: 0.4.0, nightly
Status: published

Hello, The main new things is a much improved client syntax as well as
fully functional client modules and much improved handling of "Clients".
Get it from the download section (113) or here: \*
http://files.nsclient.org/nightly/NSCP-0.4.0.113-x64.msi \*
http://files.nsclient.org/nightly/NSCP-0.4.0.113-Win32.msi \* On linux
just checkout trunk and build (see build page) I will post a guide to
getting started with 0.4.0 later tonight. // Michael Medin Full change
log:

     2011-12-06 MickeM * Fixed so command line client wont try to run commands in modules which does not support it. * Changed to when no settings is found a default one is created * Removed old "location" key from switch context and changed so it use the new number scheme 2011-12-06 MickeM * Added python unittests to make sure threading is working properly * Simpliefied and cleaned up the command line syntax a bit * Now --exec is the default option for client mode (but it will notify you it thought so) * Added "command-less" execution to PythonScript so you can do --exec --script ... (without having --exec run) * Fixed an issue related to python threading * Fixed Scheduler header propgation * Fixed so all Client module use "complex" API meaning headers are propagated correctly * Fixed scheduler alias issue 2011-11-27 MickeM * Fixed some NSCA issues (reading from new conf) * Fixed some linux build issues (related to refactoring) 2011-11-27 MickeM * Major refactoring in the command line interface * Added support for alias to many common module (command line) so: nscp eventlog (is the same as nscp client --module CheckEventLog) * Fixed issue with CheckEventLog message rendering and eventid * Refactored all Client modules to all support command line, commands and submissions. * Added uniform handling of "everything" to all Client plugins * Fixed SyslogClient to work "as advertised" (ie. all hardcoded stuff is removed) * Fixed utf8 issue with text strings (now have a working concept which needs to be implementd "all over the place") * Many issues and fixes related to clients. * Fixed so CheckEvent log (insert) works much better (added new options) 

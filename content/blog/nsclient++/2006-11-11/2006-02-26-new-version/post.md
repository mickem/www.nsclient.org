Title: 2006-02-26 New version
Author: mickem
Status: published

Alot of update in this version and a few "major" things to the socket so
verify that it works alright before you roll it out... Also note that
the SysTray has to be installed prior to use so dont forget that if you
do a new install. \* Added syntax option to CheckFile (%filename%,
%creation%, %access%, %write%, %size%). \* Fixed Sections problem (now
sections can be any size) \* Added bind\_to\_address option to both NRPE
and NSClient section in the INI file. Allows you to bind the listener to
a specific IP address (only dotted number not host name). This might
break things as I had to do some internal rewrite of the Socket classes
so be careful :) \* Disabled default-debug logging (as things are fairly
stable, you can still enable it by using debug=1 in the NSC:ini file) \*
"Fixed" socket backlog to use "max responsible value" as opposed to "10"
if no value is specified. \* Added option socket\_back\_log to both NRPE
and NSClient section that allows you to tweak the "back-log" of incoming
connections to keep. This is an advanced setting and should not be used.
If you get "connection refused" when running many client this might be
something you want to tweak though. And if you then start getting
"Socket timeout" you might wanna tweak the timeout value as well because
larger value here means it takes "longer" to process a socket. \* I have
looked into the event log problem and dates seem to work here so if
anyone still have problems (use the syntax option to debug) let me know.
\* Moved listpdh and debugpdh into the CheckSystem module \* Removed PDH
dependencies from "core exe" means you can run NSClient++ without PDH
(though you cant use the CheckSystem module) \* Added new Interface for
Modules (NSCommandLineExec that allows modules to execute things give
from command line. Syntax is NSClient++ <module name> <command>
\[arguments\] and if a module doesn't support this it is simply ignored.
\* Added new install/uninstall command to SystemTray module:
NSClient++.exe SystemTray install NSClient++.exe SystemTray uninstall
That will install/uninstall the system tray module this sets the "Allow
Service to Interact with Desktop" flag for the service. \* Removed the
"Allow Service to Interact with Desktop" flag from the /install option
so that it no longer defaults to on (see commands to set this above). \*
Fixed so checkProcess isn't case sensitive. \* Added (not finished)
syntax option to event log checker to format the outputted data

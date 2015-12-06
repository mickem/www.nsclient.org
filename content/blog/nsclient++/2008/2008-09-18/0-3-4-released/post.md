Title: 0.3.4 Released!
Author: mickem
Status: published

Just a quick shout to everyone as I have just released the 0.3.4 version of NSClient++. 
The major new things are: 

1. The new system tray that works on Vista and beyond 
2. Many fixes and improved error handling. 

A slightly more detailed list:

* Minor tweaks to CheckServiceState ("missing services" are now handled better) 
* Added some "reasonable checks under \[External Alias\] for the CheckExternalScripts.dll module.
* CheckEventLog now supports "long eventlog names" (you can now use the alias used in the event viewer) 
* '''BREAKING CHANGE''' filter=new is now the default so unless you use the new filtering you need to specify filter=old instead! 
* Brand new (but highly unstable) System tray support for windows Vista and beyond 
* SVN tree now has a sample net plugin (with C++ wrapper) 
* Installer now "uninstalls" as it "should"
* Improved error handling for the WMI checks as well as some additions.
* Fixed issue with & and : on some commands via check\_nt. 
* Added sample powershell script as well as a workaround for making them run. 
* Added DebugOutput to service handling features so if you experience trouble try using sysinternals DebugView to see logging before the agent startes. 
* Removed all (I think) asserts replacing them with exceptions (should I hope reduce crashes and instead leave some form of errors) 


Full change log for this release is here:

    2008-09-18 MickeM - 0.3.4
     * Changed so "missing services" are treated as stopped.
        CheckServiceState missing=stopped ShowAll
    	OK: missing: not found
     * Fixed issue with : in service name.
     + Added some "reasonable default cheks" under [External Alias] for the CheckExternalScripts.dll module. 
    
    2008-09-17 MickeM - 0.3.4 RC-6
     * Added option [EventLog] lookup_names=0 to disable the evetlog name lookup (default is on)
    
    2008-09-17 MickeM
     * Fixed issue on all filters so == takes the "usual" 2 equalsigns (old still works).
     * Added so tray icon can get "propper" name from core for "description".
     * Added lookup of "long" eventlog names (you can now use the alias used in the event viewer)
    
    2008-09-16 MickeM - 0.3.4 RC-5
     * Fixed an issue with the session launcher
    
    2008-09-15 MickeM
     * Fixed so NSCLient++ can load with "broken plugins" (before it printed an error and exited)
     + Added a very basic simple .net plugin (and a wrapper)
    
    2008-09-14 MickeM - 0.3.4 RC-4
     * Fixed an issue with the session launcher
     * Fixed an issue with the uninstaller (should not "fail" when problems uninstalling)
    
    2008-09-14 MickeM - 0.3.4 RC-4
     * Fixed issue with OS detection (again)
     * Fixed issue with plugin unloading (again)
     * Fixed issue with SSL socket not unloading properly
     * Fixed issue with "login" and "no session" (should work now I hope) (#222)
     * Changed so all projects build under "tmp" instead of under respecitve directory. (simpler to remove all "tmp" files now)
    
    2008-09-12 MickeM
     * Thanks to everyone who listened in on my session at NETWAYS Nagios Konferenz 2008!
    
    2008-09-09 MickeM - 0.3.4 RC-3
     * Improved error handling for the WMI checks.
     + CheckWMI: Added support for extracting numbers from strings 
     * Fixed performance data for "large float values" to be rendered without scientific notation. (#151)
     * Fixed issue with & and some commands via check_nt.
     * Fixed a crash on exit (which I added in Rc1).
     * Added 10 "bytes" the CPU buffer: (#174)
     + Added new option to [EventLog] section buffer_size to change the size of the buffer used when scanning the evenlotg (defaults to 64k).
     * Fixed error handling in CHeckEventLog so errors are repoorted properly (#184)
    
    2008-09-08 MickeM - 0.3.4 RC-2
     * Fixed issue in windows 2008 with system tray (shared_session).
     * Fixed installer issue (should run (i hope) service installer on install now on 64 bit os)
     * Fixed issue with unloading plugins and log (causing "timeouts" when exiting some times)
    
    2008-09-07 MickeM
     + Added sample powershell script as well as a workaround for making them run.
     * Fixed an issue making powershell scripts (and possibly others) not timeout properly.
     + Added upgrade support to the installer (still need to add support for keeping .ini file so be ware)
    
    2008-09-06 MickeM
     * Improved error reporting in the eventlogchecker
     * *BREAKING CHANGE* filter=new is now the default so unless you use the new filtering you need to specify filter=old instead!
       I Recomend everyone to stop using the "old" filtering.
    
    2008-09-04 MickeM
     * Fixed issues with new service stuff on NT4 and W2K (should work fine now)
     + Added some DebugOutput to service handling features so if you experience tropubel try using sysinternals DebugView too se logging before the agent startes.
     * Fixed a memory leak in the error formating code
    
    2008-08-24 MickeM
     * Changed NSCA "general problem" error message to be more descriptive.
     * Fixed issue with CheckCPU not returning a valid performance unit (%) see issue #219 for details.
    
    2008-08-16 MickeM
     * *WARNING* THIS IS VERY VERY UNSTABEL (possibly)
     * *WARNING* A lot of new untested code here so dont run in production enviornments :)
     + Added shared session so system tray can communicate with master
     + Added new system tray handlig (via TS so FUS should work with it)
     + Added new option [System] / shared_session=0 (or 1) to enable / disable the new shared memory framework (it is for now disabled by default)
       If you want to try this remember to change that option but also beware! it is dagerous and not finnished and and also there is as of now no security at all.
    
    2008-08-09 MickeM
     + Added ChangeWindowMessageFilter so systray should maybe work on vista and beyond!
    
    2008-07-28 MickeM
     * Improved the error handling for the check proc state.
     * Removed all (I think) asserts replacing them with exceptions (should I hope reduce crashes and instead leave some form of errors)
    
    2008-07-25 MickeM
     + Built a garage at the summer house
     * cut down all the reeds and shrubbs at the summer house.
    
    2008-07-03 MickeM
     * Fixed (again) issue with performance data and CheckDriveSize (when using "Min" bounds)
     + Added some more error messages for when counters are not found.
     * Fixed an issue with the new namespace option

// Michael Medin

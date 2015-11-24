Title: New nightly up!
Author: mickem
Status: published

A new nightly build up. This is an up coming 0.3.6 witch features a
brand new build system (boost build). Notice this build is still built
from within visual studio but it can be built with boost as well but
currently the renaming of the zip-file and upload has not been fixed
(which I hope to do shortly). The new version also features some
important fixes to two fairly important bugs \* Handle leak inside the
External Scripts module \* Broken CheckWMI (when no filter was
specified). It also has a '''brand new''' module for helping track down
leaks and such: \* A\_DebugLogMetrics.dll If you enable this module a
file will be created under %APP\_DATA%/nsclient++/process\_info.csv
which contains important metrics like handles, memory and such. This is
'''very helpful''' if you suspect there is a memory leak inside
NSClient++. It is important to understand that this will '''SEVERELY'''
impact performance in a negative way as all commands will be routed
through it so don't enable unless you want to check for a problem. Full
changelog is here:

     2009-01-20 MickeM * Fixed issue with CheckWMI when no filter was specified. 2009-01-17 MickeM + Added new command line option pdhlookup (to CheckSystem) to lookup index from names. Probably not usefull to anyone but me :) Usage: "nsclient++ -noboot CheckSystem pdhlookup Antal bindningsreferenser" * Fixed so PDH Collectors use the same exception as the rest of the PDH stuff (might give better errors when PDH breaks, but I doubt it) * removed debug output from -noboot + Added new command line option pdhmatch to use pattern matching on PDH queries Usage: nsclient++ -noboot CheckSystem pdhmatch Process(*)Antal trådar * Improved error reporting in the PDH subsystem. + Added new module A_DebugLogMetrics.dll which can be used to generate debug info. Enable the module and a file called process_info.csv will be created under %APP_DATA%/nsclient++/process_info.csv which contains metrics. * Fixed handle leak in CheckExternalProcess and NRPEListsner (executing commands). 2009-01-13 MickeM * Fixed issue with 64-bit installer (now installs under Program Files (and not x86) + Brand new build enviornment based upon boost build!!! Use batch file to build (release-build.bat or modify to make your own) * Modified /about so it now shows a lot of usefull(?) info. 2008-11-13 MickeM + Added truncate option to checkServiceState 2008-09-24 MickeM * Imroved the installer (now auto-updates the version when built) 

// Michael Medin

Title: 0.3.3 Released (and updated)
Author: mickem
Status: published

New build just out (not on sourceforge yet, lets see if there are any other minor fixes first). 
The updated version has a few minor quick bug-fixes. A few new things but mainly a bug fix: 

* Fixed a crash when parsing external commands. 
* Installer (i hope) will be better (in so far as w32 and x64 are "different"). 
* Namespace support for WMI. 
* Some issues with CheckDriveSize has been fixed. 
* New checks to CheckHelpers (mainly for NSCA)

Full changelog:

    2008-07-02 MickeM
     ! 0.3.3 Released (take 2)
     + Added new option alias to controll the name for performance counters when using checkfile use like so:
        checkfile alias=foo file=C:\boot.ini filter-written=>1000d syntax=gurka MaxCrit=1
     * Fixed issue with performance data and CheckDriveSize (when using "Min" bounds)
     ! 0.3.3 Released (take 1)
     * Fixed some issues (?) with the installer the w32 and x64 are now different components (GUIDs).

    2008-07-02 MickeM
     + Fixed some issues (?) with the installer the w32 and x64 are now different components (GUIDs).
    
    2008-07-01 MickeM
     + Added new option (namespace) to CheckWMI and CheckWMIValue use like so:
       CheckWMI namespace=root\\cimv2 MaxCrit=3 MinWarn=1 "Query:load=Select * from win32_Processor"
    
    2008-06-30 MickeM
     * Fixed issue with CheckFile and performance data ( #156 )
     + Added option (InvalidStatus) to CheckCounter to allow other then UNKNOWN return state when counters are missing ( #167 ).
       *NOTICE* this is all reasons (so if the counter is missing or some such the same will happen not just when the instance is missing)
       Message will reflect reason.
     * Fixed issue in the arraybuffer (one of the plit functions had a problem with multiple chars of the same) ( #190 )
    
    2008-06-25 MickeM
     * Fixed issue with CheckDriveSize and CheckAllOthers (#188)
    
    2008-06-24 MickeM
     + Added new check (to CheckHelpers): CheckOK: Just return OK (anything passed along will be used as a message).
     + Added new check (to CheckHelpers): CheckWARNING: Just return WARN (anything passed along will be used as a message).
     + Added new check (to CheckHelpers): CheckCRITICAL: Just return CRIT (anything passed along will be used as a message).
     + Added new check (to CheckHelpers): CheckVersion: Just return the nagios version (along with OK status).
     * Better error messages in the check service thingy.
    
    2008-06-18 MickeM
     * Fixed an issue in regards to reading the return packet in the in the NRPEClient (now it works).
       Before only the first 1024 bytes were used.
    
    2008-06-15 MickeM
     * Applied patches from Jeff Goldschrafe <goldschr AT cshl.edu>
       + CheckDriveSize now uses "all drives" when no drive is specified.
       * Fixed misspellt Container
    
    2008-06-14 MickeM
     * Fixed error message from external commands (better reporting now)
    
    2008-05-14 MickeM
     * Fixed memoryleak in the service checker.
         I am really sorry I usualy write better code then this.


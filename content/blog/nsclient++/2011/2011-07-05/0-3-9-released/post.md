Title: 0.3.9 Released!
Author: mickem
Tags: 0.3.9
Status: published

Yaaay, just a quick heads up 0.3.9 is now released. 
Major focus has been on CheckDrive/CheckFile as well as Crash deection/handling Some of the major changes include 

* Improvments to the where filtering: 
** case-insensetive
** regexp matching
** substring matching 
** not like 
** str(...) 
* Fixed NSCA issues 
* New commands 
** CheckFiles (replaces CheckFile/CheckFile2) 
** check_updates.vbs script 
** CheckTaskSched (using filters) 
** check_nscp 
** Negate - Timeout 
* A lot of aliases 
* CheckDisk/Drive 
** check_mk "magic" modifier 
** Proper volume support 
** ignore-unreadable 
* "hung process" detection in CheckProcState 
* Added crash handling/reporting 
* Removed: 
** CheckFile was removed (replacedby CheckFiles) 
** CheckFile2 is now deprecated 
* Fixed many issues with performance data 
* And many other things as well I still need to update various section on the wiki to describe all these new changes/additions.

Full change log:

    2011-06-28 MickeM - 0.3.9 rc5
     * CheckDisk: Fixed time comparissons for files
     * where filters: Fixed le beeing interpreted as lt
    
    2011-06-27 MickeM - 0.3.9 rc4
     * Fixed issue where parsers and () which was broken
     * Made most keywords in the where parser case insensitive so NOT and not as well as AND and AnD should now all work
     * Changed so unredable processes are debug messages (as modern windows usualy always has a few)
    
    2011-06-14 MickeM - 0.3.9 rc2
     * Fixed issue with performance data in memory check
    
    2011-06-13 MickeM - 0.3.9 rc2
     * Fixed some issues with CheckFiles
     * Added regexp matching to all string filters
       like so: "filter=message regexp '.*MICKEM-LAPTOP.*'" 
       CheckEventLog file=application file=system MaxWarn=1 MaxCrit=1 "filter=generated gt -2d AND message regexp '.*MICKEM-LAPTOP.*'" truncate=800 unique descriptions "syntax=%severity%: %source%: %message% (%count%)"
     * Fixed issue with errant "dot" in the performance data (I really hate performance data)
    
    2011-05-20 MickeM
     * Added new option to CheckprocState (ignore-state) to ignore any state checks (usefull for checking MaxCount when 0 is an option)
     * Fixed performance data for process checks.
     * Fixed error message for the op5 sales people
    
    2011-04-01 MickeM
     * Fixed (finally!!) the NSCA issue with multiple commands and missing "data"
    
    2011-03-24 MickeM
     * Added check_updates.vbs script
     * Added a lot of useful(?) aliases
    
    2011-03-22 MickeM
     * Added magic modifier (shamelessly stolen from check_mk) to CheckDriveSize
    
    2011-03-17 MickeM
     * Added proper volume support to CheckDriveSize
    
    2011-03-15 MickeM
     * Added suport for delayed start to service check (default ignored)
     * Added new option to CheckDriveSize ignore-unreadable which will ignore checking any unreadable disk drive.
    
    2011-02-16 MickeM
     * Added new module CheckTaskSched2 which is the same as CheckTaskSched but designed for Vista and beyond.
       So if you want to check "new tasks" on modern Windows use this module instead of the CheckTaskSched mosule.
       They are exactly the same excep using different APIs (and somewhat different options)
       The CheckTaskSched2 is somewhat limited as the only supported keys are: title, exit_code, status, most_recent_run_time
    
    2011-02-10 MickeM
     * Fixed issue with where filters and & operator
     * Added exact bounds to CheckTaskSched
     * Added conversion of status from string
     * Fixed time handling in CheckTaskSched to be "UTC" (hence the %most_recent_run_time% syntax string is also UTC)
     
    2011-02-01 MickeM
     ! BREAKING CHANGE!
     * Removed deprecated command CheckFile
     * Deprecated command CheckFile2
     * Added new command CheckFiles which replaces CheckFile2 and CheckFile
       Command has the new where filter syntax like so:
       CheckFiles path=D:\tmp pattern=*.exe "filter=version != 1.0" "syntax=%filename%: %version%" MaxWarn=1
     * Replaced undocumented CheckTaskSched with a new where filter based command.
       CheckTaskSched debug "filter=exit_code != 0" "syntax=%title%: %exit_code%"
    
    2010-12-26 MickeM
     * Improved crash reporter to support BOTH archive and send.
     * Improved crash reporter to archive under APPDATA (Local Settings/NSClient++/crash dumps)
     * Started on the new CheckNSCP (internal health plugin)
     * Added a "text description" file to crash dump folder to see which version crashed and what not.
     * General improvments to the crash helper.
     * Added check_nscp which is a basic command to check the internal health of NSClient++
     * Added check_files (script) submitted by 
    
    2010-12-25 MickeM
     * Fixed issue with performance coutners and erroneouse pointers in some rare cases.
       (Thank you google breakpad)
     * Added date to crash reports (to make it simpler to find correct symbols)
     
    2010-12-14 MickeM
     * CheckEventLog: Fixed so type can be compared to various string keys: error, warning, info, auditSuccess, auditFailure
     * CheckEventLog: Fixed so invalid parses are reported better (check the "rest" buffer)
        CheckEventLog file=Application "filter=generated gt -600m AND message LIKE 'Click2Run'" ...
        WARNING:Parsing failed: AND message LIKE 'Click2Run'
     * CheckEventLog: Added support for "not like" operator.
        CheckEventLog file=Application "filter=generated gt -600m AND message not like 'Click2Run'" ...
     * CrashHandler: Added several options to the crash handler (so it can be configurable)
        Everything reside under the [crash] sectiuon and the avalible keys are:
         * restart=1 # if we shall restart the service when a crash is detected.
         * service_name=<name of service to restart>
         * submit=0 # if we shall submit crash reports to crash.nsclient.org
         * url=http://crash.nsclient.org/submit
         * archive=1 # Archive crashdumps
         * folder=<appfolder>/dumps
     
    2010-12-13 MickeM
     + Added not responding detection to CheckProcState
       All "hung" processes will be considerd "hung" (and not started/stopped)
       When process is "not hung" (badapp.exe)
        CheckProcState quake.exe=stopped badapp.exe=started notepad++.exe=started
         OK:OK: All processes are running.
        CheckProcState quake.exe=stopped badapp.exe=hung notepad++.exe=started
         CRITICAL:CRITICAL: BadApp.exe: started (critical)
       Where as when it is hung:
        CheckProcState quake.exe=stopped badapp.exe=started notepad++.exe=started
         CRITICAL:CRITICAL: BadApp.exe: hung (critical)
        CheckProcState quake.exe=stopped badapp.exe=hung notepad++.exe=started
         OK:OK: All processes are running.
       
    2010-12-12 MickeM
     + Added initial support for google breakpad
       This means if nsclient++ crash two things will happen now.
       1. Crash reports will be sent to crash.nsclient.org (this will be optionalin the near future)
       2. service will restart
       You can try this out in /test mode using the "assert" command.
       
    2010-11-14 MickeM
     * Added the "extended NRPE payload packet patch"
       Should have done this years ago but alas I have not.
       This allows you to (with a patched NRPE) send and recieve more then 1024 chars (in a backwards compatible way)
       cf: https://dev.icinga.org/attachments/113/nrpe_multiline.patch
       To enable this you set the following. The value is the number of packets we allow.
       [NRPE]
       packet_count=10
       NOTICE for this to make sence you need to extend the "main payload buffer" which will most likely run out.
       [Settings]
       string_length=16000
       This value "should" be NRPE:packet_count*NRPE:string_length(1024)
    
    2010-10-17 MickeM
     * Added new command timeout which runs a command in a thread and timeouts after a given time.
       *NOTICE* this is not a good command to use since it will leak memory/resources when it "kills threads"
     * Added new command: negate which can alter the result of other commands
    
    2010-09-29 MickeM
     * Reverted a merge miss in CheckDisk
     * Added so IN (...) accepts strings without qoutes in the SQL Query syntax of CheckEventlog
     * Added new "parsing structure" str(...) to create strings in the SQL query without using ticks (') to allow "nasty meta char thingy")
     * Extended error parsing (eventlog messages) to allow up to 24 arguments (up from 11)
    
    2010-08-04 MickeM
     * Added performance data display when missing bounds
    
    2010-07-28 MickeM
     * Fixed issue with NSCA server and closing sockets (no flushes the datat before)
     * Fixed issue with performance data units beeing incorrect:
        before: B, K, M, G, ... noew: B, KB, MB, GB, ...
     * Fixed syntax errors in performance data extra ';' dropped and spaces added propperly
       Result now looks like so: ... |'C:\ %'=42%;10;5 'C:\'=229.66GB;39.06;19.53;0;390.62 'D:\ %'=99%;10;5 'D:\'=3.39GB;20.55;10.27;0;205.54
     * Fixed issues with caluclating netmask (also added support for spaces and tabs in the hostlist string.
    
    2010-06-02 MickeM
     * Fixed a few issues with listCounterInstances

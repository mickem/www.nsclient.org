Title: New nightly build: Eventlog and Configurable crash handling
Author: mickem
Status: published

Hello everyone. Also I have some DNS issues so use www.nsclient.org (not
nsclient.org). xname is broken and wont reload (as usual) so not sure
when the short hand will come back. Another little update.

     2010-12-14 MickeM * CheckEventLog: Fixed so type can be compared to various string keys: error, warning, info, auditSuccess, auditFailure * CheckEventLog: Fixed so invalid parses are reported better (check the "rest" buffer) CheckEventLog file=Application "filter=generated gt -600m AND message LIKE 'Click2Run'" ... WARNING:Parsing failed: AND message LIKE 'Click2Run' * CheckEventLog: Added support for "not like" operator. CheckEventLog file=Application "filter=generated gt -600m AND message not like 'Click2Run'" ... * CrashHandler: Added several options to the crash handler (so it can be configurable) Everything reside under the [crash] sectiuon and the avalible keys are: * restart=1 # if we shall restart the service when a crash is detected. * service_name= * submit=0 # if we shall submit crash reports to crash.nsclient.org * url=http://crash.nsclient.org/submit * archive=1 # Archive crashdumps * folder=/dumps 2010-12-13 MickeM + Added not responding detection to CheckProcState All "hung" processes will be considerd "hung" (and not started/stopped) When process is "not hung" (badapp.exe) CheckProcState quake.exe=stopped badapp.exe=started notepad++.exe=started OK:OK: All processes are running. CheckProcState quake.exe=stopped badapp.exe=hung notepad++.exe=started CRITICAL:CRITICAL: BadApp.exe: started (critical) Where as when it is hung: CheckProcState quake.exe=stopped badapp.exe=started notepad++.exe=started CRITICAL:CRITICAL: BadApp.exe: hung (critical) CheckProcState quake.exe=stopped badapp.exe=hung notepad++.exe=started OK:OK: All processes are running. 

// Michael Medin

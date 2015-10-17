Title: New nightly build with "not responding" (hung) detection
Author: mickem
Status: published

Hello, Just a quick shout since I added experimental support for
detecting "hung" applications. It is built into CheckProcState and works
much like "started" and "stopped" but it now also has a "hung" state.
You can use it like so: 1. When process (badapp.exe) is "responding"
(not hung)

     CheckProcState quake.exe=stopped badapp.exe=started notepad++.exe=started OK:OK: All processes are running. CheckProcState quake.exe=stopped badapp.exe=hung notepad++.exe=started CRITICAL:CRITICAL: BadApp.exe: started (critical) 

2\. When process (badapp.exe) is "not responding" (hung)

     CheckProcState quake.exe=stopped badapp.exe=started notepad++.exe=started CRITICAL:CRITICAL: BadApp.exe: hung (critical) CheckProcState quake.exe=stopped badapp.exe=hung notepad++.exe=started OK:OK: All processes are running. 

\*NOTICE\* this also has the automatic crash report submission built in
(so be ware!). // Michael Medin

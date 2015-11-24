Title: New w32 nightly up! (not as broken as 0.3.2 I hope)
Author: mickem
Status: published

Sorry everyone for the rather sorry 0.3.2 last month I have (due to my
water leak) not been able to spend as much time as I wanted on
NSClient++ last month so I haven't been able to fix a new version till
now. New nightly (NSClient++-Win32-20080614-1856.\*) has the mem-leak
fix as well as all the other post 0.3.1 updates such as regexp support
and working check-services and such. I shall add some patches and see if
there are any other minor things I can fix up and then try to ship a
0.3.3 during the next week. Hopefully my water leak will be sorted the
coming week and then I shall also start shipping nightlies of the new
0.4.x branch wich some pretty cool new features :) Highlights (since
0.3.1): \* New Task-schedule checker (let me know what you think of it
it is a just an idea) \* Memory leak fix!!! \* command line option for
check process \* reg-exp support for check-process \* improvments and
such here and there // Michael Medin Full changelog here:

     2008-06-14 MickeM * Fixed error message from external commands (better reporting now) 2008-05-14 MickeM * Fixed memoryleak in the service checker. I am really sorry I usualy write better code then this. 2008-04-03 MickeM * Moved COM init to "core" (from WMI module) + Added new Check command: CheckTaskSched Use like so: CheckTaskSched +filter-exit-code==1 ShowAll MaxWarn=1 MaxCrit=1 2008-03-21 MickeM + Added command line support for process checks New option: cmdLine will toggle so full command lines are used instead of just process names. + Added regular expression matching to process checks New option: match=regexp (match=strings is the default and "old" way) + Added substring matching to process checks New option: match=substr (match=strings is the default and "old" way) This is *NOT* case blind so might be hard to use, plan to add case blindness to it in the future. : Sample command: check_nt ... -v PROCSTATE -l cmdLine,match=regexp,.*exp.* -d SHOWALL * Ohh yeah... it is 2008 this year... not 2007, fixed a few entries in the :) - BREAKING CHANGE! -- Removed TOOLHELPER API as PSAPI is simpler and toolhelp is really only useful on w9x (which I don't officially support) 2008-03-20 MickeM + Added host-lookupos for NSCA server (#149) + Added option (cache_hostname=1|0) to cache the NSCA host name (Ie. only lookup once) * Fixed service check: check_nt -v SERVICESTATE -l CheckAll so it works as advertised (#150) * Fixed issue with check_nt MEMUSE/CPULOAD/UPTIME if something is "broken" they will now return an error instead of "0". (#134) Added option debug_skip_data_collection to simulate this (just for kicks) 2008-03-18 MickeM * Added some more error messages to the NSCA module * Added support for arguments to LUA module. syntax: function debug (command, args) -- args is a table with all arguments 

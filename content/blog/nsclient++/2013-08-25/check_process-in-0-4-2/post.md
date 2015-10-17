Title: check_process in 0.4.2
Author: mickem
Tags: 0.4.2, check_process
Status: published

Well, time for a slight update. Check process is now pretty much done.
So now I need to cleanup things and make sure I haven't broken too much
stuff and then I will release the first alpha version of 0.4.2.

I am quite happy with the result of check\_process and really feel
things are starting to look nice. The command works similarly to all the
other "modern" commands which means we can do:

     check_process help ... top-syntax=ARG Top level syntax. Used to format the message to return can include strings as well as special keywords such as: ${command_line}: Command line of process (not always available) ${creation}: Creation time ${exe}: The name of the executable ${filename}: Name of process (with path) ${gdi_handles}: Number of handles ${handles}: Number of handles ${hung}: Process is hung ${kernel}: Kernel time in seconds ${page_fault}: Page fault count ${pagefile}: Peak page file use in bytes ${peak_pagefile}: Page file usage in bytes ${peak_virtual}: Peak virtual size in bytes ${peak_working_set}: Peak working set in bytes ${pid}: Process id ${started}: Process is started ${state}: The current state (started, stopped hung) ${stopped}: Process is stopped ${user}: User time in seconds ${user_handles}: Number of handles ${virtual}: Virtual size in bytes ${working_set}: Working set in bytes ...

To get help. More importantly running the command without any arguments
we get:

     check_process SetPoint.exe=hung Performance data: 'taskhost.exe'=1;1;0 'dwm.exe'=1;1;0 'explorer.exe'=1;1;0 ... 'chrome.exe'=1;1;0 'vcpkgsrv.exe'=1;1;0 'vcpkgsrv.exe'=1;1;0

This will check that all running process are running (and not hung)
perhaps not that sensible but it is a good start. In my case
Setpoint.exe has hung. The performance data is not that sensible but a
list of all processes running on the system. The old kind of checks
still work:

     check_process process=explorer.exe process=foo.exe foo.exe=stopped Performance data: 'explorer.exe'=1;1;0 'foo.exe'=0;1;0

This time we only get performance data for the processes we are asking
for (and foo.exe is not running). The really cool stuff though is that
you can check aspects of processes. Here we check if explorer exe has a
working set (memory) usage above 70Mb (which it does).

     check_process process=explorer.exe "warn=working_set > 70m" explorer.exe=started Performance data: 'explorer.exe ws_size'=73M;70;0

As you can see (in the performance data) the working set is 73Mb.
Unfortunately the syntax is not dynamic so you have to change the syntax
here to get the details. But the cool thing about this is that you can
get ANY metric you want in there in addition to what you check. For
instance:

     check_process process=explorer.exe "warn=working_set > 70m" "detail-syntax=${exe} ws:${working_set}, handles: ${handles}, user time:${user}s" explorer.exe ws:77271040, handles: 800, user time:107s Performance data: 'explorer.exe ws_size'=73M;70;0

-   working set: 77Mb
-   number of handles: 800
-   number of seconds user time: 107

All this (and many many more things) can also be checked using the
fitlers and warn/crit expressions. All in all I think this is really
really neat! Please have some patience a few more days of cleaning up
loose ends and youwill be able to download the alpha version!

// Michael Medin

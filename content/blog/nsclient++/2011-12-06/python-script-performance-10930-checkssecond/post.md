Title: Python Script Performance: 10930 checks/second
Author: mickem
Status: published

This is really about Python threadsafeness I guess (but the numbers
sounds cool). I have had various issues with python through out the
development of the module (mainly related to pythons rather strange
threading model). After discovering some issues the night before the
conferance pressentation I set it upon myself to write some unit-tests
for the python script module to make sure the threads are actually safe
and works correctly. And in doing so I got some interesting numbers.

     OK: Summary Collected 109989 checks in 10 seconds: 10930/s 

At the OSMC conference the other day they presented some numbers
comparing Shinken with Nagios and Icinga and the gist of it was that
Shinken was around 4 times as fast as Nagios with Shinken running 120k
checks in 5 minutes which roughly translates to 400 checks/second. Now
in my python unit test what I do is I run an internal python based check
(forwarding the result via internal channels again to Python) but in
doing so to be able to force simultaneousness I run 50 threads pumping
around 15k checks per second. This means I get (after running around
100000 checks) an average measured from python 10930 checks per second.
This at an average 30% CPU load on my machine... And yes, this is not
fair at all, first off I have no idea what kind of hardware they used to
run their checks and neither do I do any proper service checks (in fact
running 10k+ service checks per second could actually even exhaust my
local port stash since each remote check would probably take a few
seconds). Regardless I think it shows that NSClient++ is able to
schedule a lot of checks and more importantly for me Python is now
thread safe (I hope :) )... // Michael Medin

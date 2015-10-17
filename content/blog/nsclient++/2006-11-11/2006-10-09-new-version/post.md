Title: 2006-10-09 New version
Author: mickem
Status: published

Again untested, but I haven't had time to setup a test environment since
the "hibernation" during summer... But no major changes so hopefully it
will work :) '''HUGE''' thanks to "Johnny Wetlaufer" for the logo (im
gonns do the resize a bit better in photoshop when I heve the time) !
'''Thanx''' \* Fixed a W2k3 "bug" (actually just an incorrect error) but
the: "e .PDHCollector.cpp(130) Failed to query performance counters..."
is no more... + Added option to NRPE/NSClient section to not-cache host
names (for dyndns etc.) NOTICE this is "not safe" really in so far as
someone might hi-jack your DNS and quickly gain access to your nagios
box (probably only a theoretical problem but hey! :) NOTICE this is
"slow" since all hosts in the list are "looked up" each time you get a
NRPE/NSClient request it will be "slow" but I think it is not that much
of a problem really. NOTICE I dont have the posibility to test this so
feel free to report if it works and if it doesn't. Set
cache\_allowed\_hosts=0 to disable host cache

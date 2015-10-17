Title: Nagios World Conferance and check_pagefile
Author: mickem
Tags: 0.4.2, conference
Status: published

A tiny bit of information about the 0.4.2 status. I added a new command
check\_pagefile whch will allow you to check the usage and size of your
page files.

    check_pagefile
    L client WARNING: DeviceHarddiskVolume2pagefile.sys 24.3M (32M) 
    L client Performance data: '??D:pagefile.sys'=1G;14;19;0;23 '??D:pagefile.sys %'=6%;59;79;0;100 'DeviceHarddiskVolume2pagefile.sys'=24M;19;25;0;32 'DeviceHarddiskVolume2pagefile.sys %'=75%;59;79;0;100 'total'=1G;14;19;0;23 'total %'=6%;59;79;0;100

Or you can do the usual:

    check_pagefile "filter=name = 'total'" "top-syntax=${list}" OK: total 1.66G (24G) Performance data: 'total'=1G;14;19;0;23 'total %'=6%;59;79;0;100

And help works as well:

     check_pagefile help 
    ... 
    filter=ARG Filter which marks interesting items. Interesting items are items which will be included in the check. They do not denote warning or critical state but they are checked use this to filter out unwanted items. 
    Avalible options: free Free memory in bytes (g,m,k,b) or percentages % name The name of the page file (location) size Total size of pagefile used Used memory in bytes (g,m,k,b) or percentages % count Number of items matching the filter total Total number of items ok_count Number of items matched the ok criteria warn_count Number of items matched the warning criteria crit_count Number of items matched the critical criteria problem_count Number of items matched either warning or critical criteria ...

I would also like to remind everyone that I will be presenting at
**Nagios World Conferance** next week so if your going there feel free
to bump into me!

And take the chance to listen to my talk about: **MONITORING
Simplified**

// Michael Medin

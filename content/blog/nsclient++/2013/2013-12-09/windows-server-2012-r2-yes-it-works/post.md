Title: Windows Server 2012 R2: Yes it works!
Author: mickem
Tags: 0.4.2
Status: published

Just wanted to give a quick note that yes indeed it works on Windows
Server 2012 R2...

    D core NSClient++ - 0,4,2,66 2013-12-05 Started!

    load CheckSystem 
    D core adding C:Program Filesop5NSClient++/modulesCheckSystem.dll check_cpu 
    L client OK: CPU Load ok 
    L client Performance data: 'total 5m'=0%;80;90 'total 1m'=0%;80;90 'total 5s'=2%;80;90 check_uptime 
    L client CRITICAL: uptime: 0:2h, boot: 2013-Dec-09 22:54:23 (UTC) 
    L client Performance data: 'uptime'=167;172800;86400 check_memory 
    L client OK: OK memory within bounds. 
    L client Performance data: 'committed'=0GB;2;2;0;3 'committed %'=15%;80;90;0;100 'physical'=0GB;1;1;0;1 'physical %'=24%;79;89;0;100 check_service 
    L client OK: OK all services are ok. check_os_version 
    L client CRITICAL: Windows 2012 (6.2.9200) L client Performance data: 'version'=62;50;50

I will do some more extensive tests tomorrow but looks good so far.

// Michael Medin

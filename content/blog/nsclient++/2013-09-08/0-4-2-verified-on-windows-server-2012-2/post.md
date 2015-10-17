Title: 0.4.2 verified on Windows Server 2012
Author: mickem
Status: published

And almost everything works perfectly. And with build 23 issues
mentioned here in have all been fixed so from build 23 and on wards
0.4.2 core checks are all working on all supported platforms. Next up
(not sure how much time I have this week, is check\_files and
check\_helpers)... The only major snag I noticed was check\_process
reports all running processes as "stopped". Interestingly it seems to
get the metrics such as handle count, and memory size so only the
"state" is reported incorrectly. Also I need to add so delayed services
which are not started only generates a warning (and add support for
filtering on delayed status). As well as a missing scaled for disk
performance data which I have already fixed (will be in next build). So
seems the core commands are coming along nicely. I also took the time to
add a check\_os\_version command to report and check the version of the
operating system. '''check\_os\_version:'''

     nscp nrpe -- --host 192.168.56.103 --command check_os_version Windows 2012 (6.2.9200)|'version'=62;50;50 

'''check\_cpu:'''

     nscp nrpe -- --host 192.168.56.103 --command check_cpu total>82%, total>94%|'total 5m'=0%;80;90 'total 1m'=82%;80;90 'total 5s'=94%;80;90 

'''check\_memory:'''

     nscp nrpe -- --host 192.168.56.103 --command check_memory OK memory within bounds.|'page'=531G;3;3;0;3 'page %'=12%;79;89;0;100 'physical'=530G;1;1;0;1 'physical %'=25%;79;89;0;100 

'''check\_service:'''

     nscp nrpe -- --host 192.168.56.103 --command check_service DPS=stopped (auto), MSDTC=stopped (auto), sppsvc=stopped (auto), UALSVC=stopped (auto) 

'''check\_uptime:'''

     nscp nrpe -- --host 192.168.56.103 --command check_uptime uptime: -0:3, boot: 2013-sep-08 18:41:06 (UCT)|'uptime'=1378665666;1378579481;1378622681 

'''check\_process:'''

     nscp nrpe -- --host 192.168.56.103 --command check_process smss.exe=stopped, csrss.exe=stopped, wininit.exe=stopped, ... msdtc.exe=stopped 

     nscp nrpe -- --host 192.168.56.103 --command check_process --arguments "warn=virtual > 200m" ...|' v_size'=0M;200;0 'smss.exe v_size'=4M;200;0 'svchost.exe v_size'=885M;200;0 

'''check\_memory:'''

     nscp nrpe -- --host 192.168.56.103 --command check_memory OK memory within bounds.|'page'=554G;3;3;0;3 'page %'=13%;79;89;0;100 'physical'=510G;1;1;0;1 'physical %'=24%;79;89;0;100 

'''check\_drivesize:'''

     nscp nrpe -- --host 192.168.56.103 --command check_drivesize D: > 3695179776|'C:'=10817593344;21179554201;23826998476 'D:'=3695179776;2956143820;3325661798 

'''check\_tasksched:'''

     nscp nrpe -- --host 192.168.56.103 --command check_tasksched /test: 1 != 0|'test'=1;0;0 

'''UPDATED:''' Fixed all issues mentioned here in build 23!

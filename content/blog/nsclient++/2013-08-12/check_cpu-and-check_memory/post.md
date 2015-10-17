Title: check_cpu and check_memory
Author: mickem
Tags: 0.4.2, status
Status: published

Two new commands have been modernized for 0.4.2. First off they now use
the filters which all commands should use for 0.4.2 (or at least most of
them). But they are also '''NOT''' relaying on PDH which means PDH
issues are a thing of the past! == check\_cpu == The main news for
check\_cpu apart from '''not using pdh''' and using the new filters are
that it supports checking kernels times a well as on per-core basis.
This means you can do all sorts of new things with the command. To start
you off I have some samples here to show case the new features:

     check_cpu CPU Load ok 'total 5m load'=0%;80;90 'total 1m load'=0%;80;90 'total 5s load'=7%;80;90 

This means you no longer need to provide any options for check\_cpu for
it to be help full. Out of the box it does what it usually always have
done. We can (as with all new commands) run with help to get help:

     check_cpu help help Show help screen (this screen) help-csv Show help screen as a comma separated list. This is useful for parsing the output in scripts and generate documentation etc debug Show debugging information in the log filter=ARG Filter which marks interesting items. Interesting items are items which will be included in the check. They do not denote warning or critical state but they are checked use this to filter out unwanted ... 

And we can as mentioned before get load from cores:

     check_cpu filter=none "warn=kernel > 10 or load > 80" "crit=load > 90" "top-syntax=${list}" core 0 > 3, core 1 > 0, core 2 > 0, core ... , core 7 > 15, total > 7 'core 0 5m kernel'=1%;10;0 'core 0 5m load'=3%;80;90 'core 1 5m kernel'=0%;10;0 'core 1 5m load'=0%;80;90 ... 'core 7 5s load'=15%;80;90 'total 5s kernel'=3%;10;0 'total 5s load'=7%;80;90 

What we do here is a few interesting things. 1. By default we have a
filter which says we only want the totals. Tu turn this off we set
filter=none 2. Since we have boundaries for both kernel and load we get
performance data for both as well (this is automatica, what you check
for is what you get performance data for) 3. Since we change the
top-syntax we can get the full list of data returned (and not only
problems) this is similar to the ShowAll option before. This turns into
a rather long list so be aware of NRPE/NSCA payload limits if you start
checking all cores with a lot of values. 4. In addition to the
individual cores we also get the value for the totals (which is what we
had before). == check\_memory == Works similarly to check\_cpu and is
also no longer dependent on PDH which means PDH issues are a thing of
the past. There are no major new changes to check\_memory apart from the
new filters which works like this. First off running without arguments
gives you a sensible default:

     check_memory OK memory within bounds. 'page used'=8G;19;21 'page used %'=33%;79;89 'physical used'=7G;9;10 'physical used %'=65%;79;89 

We can also add help to get detailed information on all command line
options:

     check_memory help help Show help screen (this screen) ... empty-state=ARG Return status to use when nothing matched filter. If no filter is specified this will never happen unless the file is empty. Default value: empty-state=unknown top-syntax=ARG Top level syntax. Used to format the message to return can include strings as well as special keywords such as: ${free}: Free memory in bytes (g,m,k,b) or percentages % ${size}: Total size of memory ${type}: The type of memory to check ${used}: Used memory in bytes (g,m,k,b) or percentages % ... 

As before performance data is automatic and generated based on the
query. In addition to this the "message" is not based on the query which
means you can customize this to return different data from the
performance data (see below where we have used size in the message and
free in the performance data). In this example we also set top-syntax to
force display the results (like ShowAll) even though they are not in
error.

     check_memory "warn=free < 20%" "crit=free < 10G" "top-syntax=${list}" page > 8.05G, physical > 7.85G 'page free'=15G;4;2 'page free %'=66%;19;9 'physical free'=4G;2;1 'physical free %'=34%;19;9 

Lastly we can use the syntax options to show any number of details back
in the message:

     check_memory "top-syntax=${list}" "detail-syntax=${type} free: ${free} used: ${used} size: ${size}" page free: 16G used: 7.98G size: 24G, physical free: 4.18G used: 7.8G size: 12G 

So there we have it. Next up is pdh counters (checking them) as well as
process/service checks, and with some luck we will have some status
updates on that in the next few days. '''Finally a question:''' Is
anyone using check\_uptime? It is the remaining PDH based check so I am
thinking of removing it in favor of a PDH free solution? // Michael
Medin

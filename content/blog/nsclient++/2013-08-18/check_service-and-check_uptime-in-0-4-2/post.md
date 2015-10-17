Title: check_service and check_uptime in 0.4.2
Author: mickem
Tags: 0.4.2
Status: published

Since I am working as hard as I can to finish the new checks for the
upcoming 0.4.2 I will not be responding to much on the support front. If
it is urgent please let me know and I will deal with it or please bare
with me for about one more week. I still hope to release the very first
alpha version in the next few days. Thus far I have already covered
check\_cpu, check\_mem, check\_pdh as well as check\_drivesize. This
time it is time for check\_service and check\_uptime. The last and final
check left int he windows check subsystem is check\_process which is a
lot of work as it requires a lot of new API plumbing. But I still hope
to have it finished this week. After that I need to run some sanity
checks on all old checks to make sure they still function as expected.
There is not much you to say about check\_uptime as it is a very simple
check. Without any arguments you get:

     check_uptime uptime: -9:02, boot: 2013-aug-18 08:29:13 'uptime uptime'=1376814553s;1376760683;1376803883 

This reads as last reboot was 9 hours 20 minutes ago. or more precisely
08:29 this morning. The performance data is as always time since epoch i
seconds. The default warning is 24 hour and critical is 12. This can as
always be changed like so:

     check_uptime "warn=uptime < -2d" "crit=uptime < -1d" ... 

Check service is a lot more involved as it has more need of the filters.
And I think it really is a nice way to showcase the power of the new
filters and how powerful the new checks are but since I have covered
much of this already in previous posts I will be brief here: The default
command:

     check_service OK all services are ok. 

The default crit/warn look a bit different: \* "warn=not
state\_is\_soft\_ok()" \* "crit=not state\_is\_ok()" This is because the
lengthy expression involved in calculating "good" states which is
resolved using the matrix below. The difference between the soft version
is that it considers service in starting state as well. || Configured
start || Expected state || || Autostart || Running || || On demand ||
ignored || || Disabled || Stopped || But this can be customized and
tweaked if you desire something else and since the filter now allows
filtering on service name, description as well as state and configured
startup etc etc. I hope this will cover all requests for new features.
There are also a few new options chief among them is "computer" which
allows you to specify a remote computer name to check remote hosts
("passively") this is a trend and will become the main focus of 0.4.3.
As always we can use the help option to get a full list of options and
descriptions (here is a few of them):

     check_Service help ... computer=ARG The name of the remote computer to check service=ARG The service to check, set this to * to check all services type=ARG The types of services to enumerate available types are driver, file-system-driver, kernel-driver, service, service-own-process, service-share-process Default value: type=service state=ARG The types of services to enumerate available states are active, inactive or all Default value: state=all 

To given a slightly more advanced use-case lats assume we want to get
the status of all auto-start services except except Bonjour Service and
Net Driver HPZ12. Then we can do the following we can do:

     check_service "filter=start_type = 'auto' and name not in ('Bonjour Service', 'Net Driver HPZ12')" "top-syntax=${list}" "detail-syntax=${name}: ${state}" AdobeActiveFileMonitor10.0: running, AdobeARMservice: running, AMD External Events Utility: running, ... wuauserv: running 

As I said initially the last check to get a makeover is check\_proc
which I shall start on tomorrow. // Michael Medin

Title: Guides and tutorials on my personal blog
Author: mickem
Tags: tutorial
Status: published

Hello, For those of you who don't already know it I have a personal blog
where I occasionally post guides and tutorials for how to use NSClient++
(and other things). The main reason to keep them apart is that trac is a
horrible blogging platform :) Thus far I have posted the following
(relevant) entries: ==
\[http://blog.medin.name/2012/09/09/self-resetting-event-log-alerts/
Self-resetting event log alerts\] == Take your monitoring to the next
level by creating self-resetting event log checks. Sometimes it is not
only faults which can be harvested from the windows event log many
applications will also report a message when the state returns to
normal. This tutorial show you how to configure NSClient++ 0.4.1 to
setup auto resetting event log checks. In addition to using passive
checks via NSCA I will also demonstrate how to use the Cache module to
benefit from real time event log checks via NRPE. ==
\[http://blog.medin.name/2012/03/20/real-time-event-log-monitoring-with-nsclient/
Real time event-log monitoring with NSClient++\] == Monitoring the event
log can quickly become straining for both the computer as well as the
administrator as the event log grows and grows. To make this simpler for
both the administrator and the computer NSClient++ 0.4.0 introduced
real-time event log monitoring. This means we no longer scan the event
log instead we simply scan events as they come in. The benefit, in
addition to lowering the resources required, is that we can also get
notified instantly when an error occurs instead of every 5 minutes or
however often we check the log. Another addition is a simple client o
generate event log message to help administrators debug event log
filters. This is a quick introduction to event log monitoring and
real-time event log monitoring showing how to set up real-time event log
monitoring both for active and passive use via NSCA and NRPE. ==
\[http://blog.medin.name/2012/03/09/using-wmi-with-nsclient-0-4-0-part-1-command-line-tools/
Using WMI with NSClient++ 0.4.0 Part 1: Command line tools\] == This is
a series detailing how you can leverage WMI to monitor you Computers
from a monitoring tool such as Nagios or Icinga. Since I decided to
clean up the command line syntax of the WMI plugin for NSClient++ for
the up-coming 0.4.0 version a few days ago I will start by showing how
you can use what has become an almost full featured WMI client. I will
try to keep this side updated as I have added a new section to the
guides: \[\[wiki:doc/usage/checks\]\] Where I (and other so feel free to
share your own blog postings there) post the links. ==
\[http://blog.medin.name My blog\] == To see all my monitoring related
entries on my blog you can go to:
\[http://blog.medin.name/category/monitoring/\] or you can read all
entries (even non monitoring related ones) here
\[http://blog.medin.name\] // Michael Medin

# About NSClient++

NSClient++ (nscp) aims to be a simple yet powerful and flexible monitoring daemon. It was built for Nagios/Icinga/Naemon, but nothing in the daemon is Nagios/Icinga specific and it can and is used in many other scenarios where you want to receive/distribute check metrics. It is entirely possible to use it stand alone as well as the core monitoring system though that is not recommended as it is rather limited.

##  What does it do?

NSClient++ does basically three things:

* Allow remote checks
  Allow a remote machine (monitoring server) to request commands to be run on this machine (the monitored machine) which return the status of the machine.
* Monitor system in realtime
  Monitor your systems and submit the findings and results a remote (monitoring server).
* Resolve your problems
  NSClient++ can take action either on its own monitoring or remotely from a central server and act on what happens and resolve issues.

##  What monitoring systems does it support?

While NSClient++ was designed to work with Nagios/Naemon/Icinga it can easiily be adapted to be used with any monitoring or information system.

* NRPE (Nagios Remote plugin Executor)
* NSCA (Nagios Service Check Acceptor)
* NRDP
* Syslog
* Graphite
* SMTP
* CollectD
* REST
  
##  Where does it run?

NSClient++ should run on most operating systems.

* Windows XP and above
* Most linux os:es

## Who is behind NSClient++?

NSClient++ is largely written and maintained by **Michael Medin**.
He uses `My Computer Solutions NORDIC KB` as a company to handle the legal and financial aspects of the project.

Contacting the project can be done via email `info@nsclient.org` or on the following address:
```
Michael Medin
My Computer Solutions NORDIC KB
Knipvägen 179
SE-184 62 ÅKERBERGA
SWEDEN
```

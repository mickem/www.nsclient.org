Title: About NSClient++
page_order: 1

NSClient++ (nscp) aims to be a simple yet powerful and flexible monitoring daemon. It was built for Nagios/Icinga/Naemon, but nothing in the daemon is Nagios/Icinga specific and it can and is used in many other scenarios where you want to receive/distribute check metrics. It is entirely possible to use it stand alone as well as the core monitoring system though that is not recommended as it is rather limited.

#  What does NSClient++ do?

NSClient++ does basically three things:

* Allow remote checks
  Allow a remote machine (monitoring server) to request commands to be run on this machine (the monitored machine) which return the status of the machine.
* Monitor system in realtime
  Monitor your systems and submit the findings and results a remote (monitoring server).
* Resolve your problems
  NSClient++ can take action either on its own monitoring or remotely from a central server and act on what happens and resolve issues.

#  How does NSClient++ monitor?

NSClient++ is designed to be open ended and allow you to customize it in any way you design thus extensibility is a core feature. NSClient++ has built-in checks for core system metrics but the real power comes from plugins and external scripts.

* External Scripts
  External scripts are scripts you write in your favorite language and are executed by NSClient++ and the results are sent back to the central monitoring server or other scripts to take action.
  This is generally the simplest way to extend NSClient++ as you can utilize whatever infrastructure or skill set you already have.
* Lua Scripts
  Lua is a scripting language much like anything you could use as an external scripts. The benefit to using “internal scripts” are that they run inside NSClient++ and can become more intelligent.
  This is the best option if you want to allow the script to run on any platform with as little infrastructure as possible yet still allow them to be extensions to NSClient++ and not just “dumb scripts”.
* Python Scripts
  Python is another internal scripting language much like lua.
  Python is an easy and powerful language which has many extensions and modules to allow you to do pretty much anything.
* .Net (dot-net)
  Dot-net modules are similar to Native modules below but written on the dot-net platform.
  This allows you to write components on top of the large dot-net ecosystem.
* Modules
  This is the most hard-core way to extend NSClient++ and will require youto compile them to work.
  Most functionality in NSClient++ is actually built as modules when you install it.

#  What does NSClient++ support?

Since NSClient++ was designed to work with Nagios /Naemon/Icinga it has support for the various protocols used by them but in addition to thos it also supports a series of other ptotocols.

* NRPE (Nagios Remote plugin Executor)
  A Nagios centric protocol to collect remote metrics (active checks).
* NSCA (Nagios Service Check Acceptor)
  Another Nagios centric protocol for submitting results (passive checks).
* NRDP
  A Nagios replacment for NSCA.
* check_mk
  Is a protocol utilized by the check_mk monitoring system.
* Syslog
  A protocol primarily designed for submitting log records to central servers.
* Graphite
  Graphite is a graphing solution which allows you do real-time graphing.
* SMTP
  SMTP is used for sending email (this more of a toy currently).
* CollectD
  A protocol for collecting information
* REST
  Web based easily firewalled protocol.
  
  
#  Where does NSClient++ run?

NSClient++ should run on the following operating systems:

## Windows
* NT4 SP5 (pre 0.4.2)
* Windows 2000 (pre 0.4.2)
* Windows XP
* Windows 2003
* Windows Vista
* Windows 2008
* Windows 7
* Windows 2012
* Windows 8
* Windows 2012 R2
* Windows 8.1
* Windows <NEXT> (NSclient++ tends to work on most versions of Windows)

## Linux
* Debian
* Centos
* Ubuntu
* Possibly others as well
  
## Plattforms
* 32bit OSes
* Amd64/x64 plattforms.
* Possibly other Linux based architectures as well

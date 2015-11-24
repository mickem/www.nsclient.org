Title: 0.4.0 Rc4 - build 148 (The last RC?)
Author: mickem
Tags: 0.4.0, release-candidate
Status: published

Well, a few bugs got caught and fixed and I managed to add a bunch of
test cases for event log checking as well. Nothing major but please
please est and let me know. If no new bugs pop up this will become 0.4.0
in a bit... Full change log

     2012-03-20 MickeM * Fixed alias/service name for real-time event log filters * Added smtp/syslog and graphite clients to installer * Fixed so eventlog wont crahs on invalid messages 2012-03-19 MickeM * Fixed issue in installer and "Make file writable" by everyone now uses Users SID. * Fixed issue in installer and "Default plugins" now correctly sets them to 1. 2012-03-18 MickeM * Removed dependency on tcpip from the service and the installer * Added new command to EventLog CheckEventlogCached which checks result caught by the real-time process. CheckEventLogCACHE warn=gt:1 crit=gt:5 Requires a configured real-time checker to work. * Added a series of keywords to EventLog check to facilitate better checking * Added a set of aliases to make EventLog behave more like Wdinwos Eventlog viewer. * Added a lot of unit test cases to the Eventlog checker. * Fixed issue with default schedule beeing added as an item and not a template 

Title: 0.3.4 RC-4 out!
Author: mickem
Status: published

Fixes a few small but all so important issues. The issues here has lead
me to believe I need to do some more testing so I will wait a bit more
for a release. But please please try it out and report back bugs. Would
be nice to have a "working" 0.3.4 without any bugs :) Changelog (since
last I posted: RC-2)

     2008-09-14 MickeM - 0.3.4 RC-4 * Fixed issue with OS detection (again) * Fixed issue with plugin unloading (again) * Fixed issue with SSL socket not unloading properly * Fixed issue with "login" and "no session" (should work now I hope) (#222) * Changed so all projects build under "tmp" instead of under respecitve directory. (simpler to remove all "tmp" files now) 2008-09-12 MickeM * Thanks to everyone who listened in on my session at NETWAYS Nagios Konferenz 2008! 2008-09-09 MickeM - 0.3.4 RC-3 * Improved error handling for the WMI checks. + CheckWMI: Added support for extracting numbers from strings * Fixed performance data for "large float values" to be rendered without scientific notation. (#151) * Fixed issue with & and some commands via check_nt. * Fixed a crash on exit (which I added in Rc1). * Added 10 "bytes" the CPU buffer: (#174) + Added new option to [EventLog] section buffer_size to change the size of the buffer used when scanning the evenlotg (defaults to 64k). * Fixed error handling in CHeckEventLog so errors are repoorted properly (#184) 

// MickeM

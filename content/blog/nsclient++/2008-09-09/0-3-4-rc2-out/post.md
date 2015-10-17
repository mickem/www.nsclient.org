Title: 0.3.4 RC2 out!
Author: mickem
Status: published

Did a few fixes as well as close and round off a lot of tickets. Fixes
in this release are:

     2008-09-09 MickeM * Fixed issue with & and some commands via check_nt. * Fixed a crash on exit (which I added in Rc1). * Added 10 "bytes" the CPU buffer: (#174) + Added new option to [EventLog] section buffer_size to change the size of the buffer used when scanning the evenlotg (defaults to 64k). * Fixed error handling in CHeckEventLog so errors are reported properly (#184) 

// MickeM

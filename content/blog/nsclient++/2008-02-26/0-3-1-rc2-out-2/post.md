Title: 0.3.1 RC2 out!
Author: mickem
Status: published

I sort of skipped RC1 (or at least I never posted it) anyways here is a
spanking brand new one which actually is not that new. Main new things
are; \* the installer (Yaaaay!) it is just a quick hack so don't expect
much. \* the NRPE client module now works as a "check command" (so now
you can check other things from nsclient++) \* and some fixes here and
there (notably NSCA modules return code) '''The change log:'''

     2008-02-26 MickeM + Added installer 2008-02-22 MickeM * Fixed issues in the NRPE module (now returns the correct status) + Added a lot of "error log" for when the packet size in NRPEListener is not correct (might make it simpler to diagnose problems) 2008-02-20 MickeM + Added new module NRPEClient that can act as a NRPE client, might be useful for testing things and eventually for relaying events. Usage: nsclient++ -noboot NRPEClient -H 192.168.0.1 -p 5666 -c check_something -a foo bar This is an early concept so don't expect much... * Fixed a bug in NSCA module (now it works again :) + Added a command wrapper for the NRPECLient module so now it can act as a check command. (No argument handling yet though), For a sample check out the [NRPE Client Handlers] section in NSC.ini 

'''UPDATE''' Yes I know, the x64 installer build is broken... sorry,
will fix tonight... :( // MickeM

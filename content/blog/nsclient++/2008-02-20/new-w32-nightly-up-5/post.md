Title: New w32 nightly up!
Author: mickem
Status: published

A few tweaks and fixes and some new stuff (nothing spectacular) \* New
option System/NRPE section: string\_length can be used to tweak return
buffer size (for 0.4 we will rewrite so this is more dynamic) With this
option you can set the return data for NRPE to be larger then the
default 1024 bytes '''but''' this requires you to recompile the NRPE
agent. \* Improvements to the PDH mutexes. Should be able to handle more
load, and better, handle situations where the load becomes to high. \*
Some improvements to the NSCA plug in (should work better now) \* Re
factored and improved the external command handling. Should be better
and more secure now as well as handle "long output". \* New module:
NRPEClient to run NRPE queryes from the CLI (will soon have support for
running NRPE queries from within NSClient++ (ie act as a proxy). We are
starting to come up on the 3.1 release so now would be a good time to
report all bugs and problems, expect 3.1 RC during the week end and
hopefully a 3.1 release end of month. == Changelog ==

     2008-02-19 MickeM + Added new module NRPEClient that can act as a NRPE client, might be useful for testing things and eventually for relaying events. Usage: nsclient++ -noboot NRPEClient -H 192.168.0.1 -p 5666 -c check_something -a foo bar This is an early concept so don't expect much... 2008-02-19 MickeM + Fixed a buffer overflow in the NRPE socket handling. 2008-02-18 MickeM + Added proper output handling to process subsystem (now you can execute programs tat return "much" data. + Added select support for SSL_write (now you can send "any amount of data" to the (SSL) socket. Since check_nrpe doesn't do this it wont work in that end, but still... 2008-02-16 MickeM + Re factored ExternalCommand handling so NRPE and new module does the same thing. 2008-02-14 MickeM + Added so commands starting in host_ (NSCA Handlers) are sent as host-commands * Fixed a copy constructor in NSCA Commands (now service checks are sent as service checks) 2008-02-13 MickeM + Added string_length to [Settings] as well (used internally) for all "injected" buffers. * Fixed issue with scripts result truncated after 1024 chars (now they return "all" output and thus you can use the NRPE settings I added yesterday :) + Added hostname setting to [NSCA] section (must have been when I did not add it before) + Added to NSCA truncates output when to long. 2008-02-12 MickeM + Added new option for the [NRPE] section string_length which is the length of the NRPE strings (notice you need to recompile the check_nrpe to match this value) * Improved exception handling in the PDH collector (hopefully less deadlocks) 

// MickeM

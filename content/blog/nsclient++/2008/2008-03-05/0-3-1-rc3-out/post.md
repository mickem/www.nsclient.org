Title: 0.3.1 RC3 out!
Author: mickem
Status: published

New RC out but nothing major, installer has some tweaks, and a few
fixes/additions in the eventlog module. Sorry for the delay, but I was
away at High Voltage Festival in Hanau and another gig in Köln enjoyed
some nice powernoise instead of coding last weekend :) The change log:

     2008-03-05 MickeM + Added debug to new section [Eventlog], when enabled it will (log) wat lines matched what, this is a pretty big performance overhead so dont run with this one. + Added syntax to new section [Eventlog] used as a shorthand for the syntax to use as "default" (when no syntax=... option is given) * Fixed an issue with eventlog and . matching. + Added shorthand ! for != in "all" numeric filters (eventlog) + Added <> (same as ! and !=) as NRPE breaks the use of ! (in "all" numeric filters (eventlog)) Try using: filter-eventType=<>warning to remove everything that is not a warning * Fixed two spelling misstakes in the SysTray module. * Fixed 64-bit issues with installer * Fixed so installer uninstalls/installs the service 

// MickeM

Title: New nightly up!
Author: mickem
Status: published

New experimental build system as well as some fixes. I need to check
linkage and such and make sure it wont require a lot of 3:d party
modules so use with care. It also features a 16bit support for
CheckProcState as well as a complete rewrite to make the process
enumeration better faster and perhaps most of all safer.

     2009-01-23 MickeM * Cleaned up the checkProcState code and it is not a lot better. - Removed race conditions (crashes?) as well as improved perfoamnce and better error handling. + Added new option 16bit to checkProcState. When set checkProcState will enumerate all 16 bit processes found running under NTVDM. * Fixed NRPE version reported "incorrectly". (Version is now takedn from NSClient++) 2009-01-21 MickeM + Added experimental 16 bit process support to checkProcState 

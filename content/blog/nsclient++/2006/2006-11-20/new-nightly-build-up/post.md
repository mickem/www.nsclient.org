Title: New "nightly" build up
Author: mickem
Status: published

Build scripts now automagically uploads the built files to the server so
hopefully the "nightly" directory will show builds more rapidly then
before, at least it is simpler for me to manage uploads :) Fixes in this
version:

     2006-11-18 MickeM + Added support for empty NRPE checking (i.e.. chec_nrpe without a -c argument) * Added error message when detected language is missing from counters.defs + Added Swedish locale to counters.defs (yes, I switched to Swedish XP on my computer :) * Fixed : (and possibly other problems) in counters when checking from check_nt (via NSCLient protocol) + Added CheckAllExcept to CheckDrive to check all except the specified drives. * Fixed a display error in the various size functions (1000-1024 byte was displayed incorrectly) 

// MickeM

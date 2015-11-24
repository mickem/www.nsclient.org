Title: 0.2.6 Released
Author: mickem
Status: published

New version released, basically same as the nightly (changed the
version). For users of 0.2.5 this is a major upgrade, not in terms of
features but since it is no built on vc++ 8.0 it might have
compatibility issues. Changes since last builds are:

     2006-12-02 MickeM + Managed to build so it works on NT 4.0 (SP6a) and W2K3 * Fixed "broken password check" in NSClient listener 2006-11-18 MickeM + Added support for empty NRPE checking (i.e.. chec_nrpe without a -c argument) * Added error message when detected language is missing from counters.defs + Added Swedish locale to counters.defs (yes, I switched to Swedish XP on my computer :) * Fixed : (and possibly other problems) in counters when checking from check_nt (via NSCLient protocol) + Added CheckAllExcept to CheckDrive to check all except the specified drives. * Fixed a display error in the variouse size functions (1000-1024 byte was displayed incorrectly) 

Please let me know if it works or not... and report bugs on the track
website http://trac.nakednuns.org/nscp/ as I am trying to organize
everything there. Next "major release" is some time during the end of
the year, which will have some more actual changes and not just a new
build platform. Feel free to request features and enhancements till
then. // MickeM

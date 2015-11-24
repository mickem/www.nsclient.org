Title: 0.3.9 RC2 is finally out!
Author: mickem
Status: published

Sorry for the delay (about one month to late) but here it is anyways.
Nothing major in this new RC but some fixes and additions.

     2011-06-13 MickeM * Fixed some issues with CheckFiles * Added regexp matching to all string filters like so: "filter=message regexp '.*MICKEM-LAPTOP.*'" CheckEventLog file=application file=system MaxWarn=1 MaxCrit=1 "filter=generated gt -2d AND message regexp '.*MICKEM-LAPTOP.*'" truncate=800 unique descriptions "syntax=%severity%: %source%: %message% (%count%)" * Fixed issue with errant "dot" in the performance data (I really hate performance data) 2011-05-20 MickeM * Added new option to CheckprocState (ignore-state) to ignore any state checks (usefull for checking MaxCount when 0 is an option) * Fixed performance data for process checks. * Fixed error message for the op5 sales people 

Since there was nothing major reported for RC1 I will if nothing major
pops out in the next few days probably release 0.3.9 final over the
weekend so please try it out before then and let me know any issues...
// Michael Medin

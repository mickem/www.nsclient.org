Title: A small x-,mas update to 0.4.1 (new nightly)
Author: mickem
Tags: 0.4.1
Status: published

Just released a new nightly build which adds two new features: 1. New
option for CheckEventLog scan-range to help combat issues with high
memory usage, high CPU load and/or similar issues. The option can be
used to reduced the entries scanned when scanning the event log and mor
importantly start scanning from the end do if you have large enevtlogs
this will save you a lot of computing time. Essentially if you set
scan-range=-2d the log will be read backwards and as soon as an entry
older then 2 days is found it will stop scanning. The potential drawback
is that there is no guarantee that entries are ordered so setting this
close to your filters might miss entries. 2. A minor change which will
create an error when a duplicate command is added which makes it simpler
to detect aliases which override internal commands. Change log:

     2012-12-25 MickeM * Added option scan-range to CheckEventLog. This new option reduces the entries scanned a *lot* and can help solve memory, time and CPU issues. The idea is that is negative we start scanning from the end and once we hit something outsiden the range we stop scanning. There is a chanse that entries reported are "outside" the range so set range bigger then generate/written date/times (to reduce this risk). CheckEventLog file=application file=system MaxWarn=1 MaxCrit=1 "filter=generated gt -1h AND level eq 'info'" truncate=800 unique descriptions "syntax=%severity%: %source%: %message% (%count%)" Executes in 7 seconds adding scan-range=-5h executes in 0 seconds (yields the same result). * Added error message when overriding a commad (ie. when alias check_cpu overrides the new command check_cpu). Wont work (for technical reasons) for duplicate aliases ie.- alias x=foo and x=bar 

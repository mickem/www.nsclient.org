Title: New release candidate for 0.4.1
Author: mickem
Tags: 0.4.1, release-candidate
Status: published

Hello, a few bug fixes and minor improvements to the 0.4.1 branch ready
for testing. If nothing major is reported I will release this in a few
days. Highlights: \* New option which can drastically improve
CheckEventLog performance scan-range \* Sample config with "all" options
\* Encoding support for NRPE \* No more loading issue in PythonModule if
python is not installed. \* Some additional bug fixes // Michael Medin
Full change log:

     2013-01-17 MickeM * Added nsclient-full.ini with "all" (non advanced) avalible options. * Fix for reloading settings from file from script: core:reload('settings') will not work. Notice it still will onlya reload the settings not the modules so modules have to be reloaded manually. * Fixed return code issue in nsclient-ini full generator. 2013-01-13 MickeM * Fixed crash when collector thread is not started. 2013-01-02 MickeM * Fixed message dialog when loading PythonScript module without python installed. * (re)add check_fiulesize which was accidentally removed. * Fix for http settings * fix for --version command line option 2012-12-28 MickeM * Reverted default NRPE encoding to "system" (not UTF-8). * Added new option to configure NRPE encoding: [/settings/NRPE/server] encoding = utf8 Valid values are currently system and utf8 (and strangely enough utf7). If you need something else let me know. 2012-12-25 MickeM * Added option scan-range to CheckEventLog. This new option reduces the entries scanned a *lot* and can help solve memory, time and CPU issues. The idea is that is negative we start scanning from the end and once we hit something outsiden the range we stop scanning. There is a chanse that entries reported are "outside" the range so set range bigger then generate/written date/times (to reduce this risk). CheckEventLog file=application file=system MaxWarn=1 MaxCrit=1 "filter=generated gt -1h AND level eq 'info'" truncate=800 unique descriptions "syntax=%severity%: %source%: %message% (%count%)" Executes in 7 seconds adding scan-range=-5h executes in 0 seconds (yields the same result). * Added error message when overriding a commad (ie. when alias check_cpu overrides the new command check_cpu). Wont work (for technical reasons) for duplicate aliases ie.- alias x=foo and x=bar 

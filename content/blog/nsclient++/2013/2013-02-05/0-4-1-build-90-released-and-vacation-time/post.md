Title: 0.4.1 (Build 90) released! (and vacation time)
Author: mickem
Tags: 0.4.1, release
Status: published

Hello, A new build (0.4.1.90) (build means bug fixes and minor tweaks) is out: 

The following new features: 
* nsclient-full.ini is now whipped with the installer to give you some copy-pasting inspirations. 
* Reload support from script (if you want to reload config in runtime) 
* Encoding support for NRPE 
* scan-range for CheckEventLog to severely reduce the load and resources required when checking eventlog. 

As well as some bugfixes for details see the full changelog below. 
I would also take this opportunity to say I will be vacationing for the next month so don't expect much in the ways of updates or changes or fixes (or
answers) in that period. 
If it is urgent please email me (michael AT medin DOT name) and I will try to respond as quickly as possible (please tag email with NSCP or NSClient++ to reduce risk of it being ignored).
Also if you haven't noticed I did some 0.4.2 commits yesterday which is the fruit of a massive refactoring effort to add documentation and new command line parser for all internal commands, very nice now you can do:

    check_eventlog --help 

To get help! 

Full changelog:

    2013-01-21 MickeM
     * Fixed two include files issues
    
    2013-01-19 MickeM
     * Fixed Wix 3.7 and added wix to dependencies
    
    2013-01-17 MickeM
     * Added nsclient-full.ini with "all" (non advanced) avalible options.
     * Fix for reloading settings from file from script: core:reload('settings') will not work.
       Notice it still will onlya reload the settings not the modules so modules have to be reloaded manually.
     * Fixed return code issue in nsclient-ini full generator.
     * Added support for delayed reloading
    
    2013-01-13 MickeM
     * Fixed crash when collector thread is not started.
    
    2013-01-02 MickeM
     * Fixed message dialog when loading PythonScript module without python installed.
     * (re)add check_fiulesize which was accidentally removed.
     * Fix for http settings
     * fix for --version command line option
    
    2012-12-28 MickeM
     * Reverted default NRPE encoding to "system" (not UTF-8).
     * Added new option to configure NRPE encoding:
        [/settings/NRPE/server]
        encoding = utf8
       Valid values are currently system and utf8 (and strangely enough utf7). If you need something else let me know.
    
    2012-12-25 MickeM
     * Added option scan-range to CheckEventLog.
       This new option reduces the entries scanned a *lot* and can help solve memory, time and CPU issues.
       The idea is that is negative we start scanning from the end and once we hit something outsiden the range we stop scanning.
       There is a chanse that entries reported are "outside" the range so set range bigger then generate/written date/times (to reduce this risk).
         CheckEventLog file=application file=system MaxWarn=1 MaxCrit=1 "filter=generated gt -1h AND level eq 'info'" truncate=800 unique descriptions "syntax=%severity%: %source%: %message% (%count%)"
       Executes in 7 seconds adding scan-range=-5h executes in 0 seconds (yields the same result).
     * Added error message when overriding a commad (ie. when alias check_cpu overrides the new command check_cpu).
       Wont work (for technical reasons) for duplicate aliases ie.- alias x=foo and x=bar


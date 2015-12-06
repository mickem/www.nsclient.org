Title: 0.3.7 Released
Author: mickem
Tags: 0.3.7, release
Status: published

New version out mainly a fix for the problems of 0.3.6 version. Major
changes:

* Added argument support to NRPE Client * Some additions and fixes CheckWMI 
* Improved installer (works on w2k8 etc) * NSCA feature and stability improvments 
* New command line switchs to easily use NSClient++ from external scripts 
* Added "firewall exception" to installer * Fixed an issue with the socket data buffer 
* Fixed issue with CheckExternalScripts and script_dir 
* Fixed issue with CheckDisk and paths 
* Documentation! 

I think the major thing is the documentation apart from some bug fixes
and installer improvements such. Regardless it is a recommended update.
'''NOTE''' It is late so I shall update sourceforge and what not
tomorrow. 

    2009-10-11 MickeM
     + Added argument support to NRPE Client
       This is temporarily enabled by the same options under the NRPE section. BUT this will change int he future so be ware when using them.
    
    2009-09-20 MickeM
     * Fixed alias in CheckWMI (now works)
     + Added columnSyntax to CheckWMI to allow formating of returned data (default is %column%=%value%)
     + Added columnSeparator to CheckWMI to allow formating of returned data (default is ", ")
    
    2009-09-13 MickeM
     * Fixed some more issues with the installer should not "work" on Windows 2008 as well as slightly simpler to configure.
    
    2009-09-06 MickeM
     + Added new option to [NSCA Agent] string_length=<size> of the NSCA_MAX_PLUGINOUTPUT_LENGTH option on the NSCA server.
     * Readded all the "installer configuration" crap which I accidentaly removed when I fixed the installer... *sigh*
    
    2009-08-30 MickeM
     + Added -c and -d command line options like so:
       NSClient++ -c CheckFile2 path=c:\test pattern=*.txt MaxCrit=1 filter+written=gt:2h
       NSClient++ -c <command> <argument 1> <argument 2> ...
       -d Is the same thing but with debug enabled.
     + Added uninstall of old client (sort of broken but works)
    
    2009-08-29 MickeM
     * Fixed issue with CheckFile (directory)
     * Rewrote the CA:s in the installer to work "better" (hopefully) in general it should be have more like a propper installer.
    
    2009-07-18 MickeM
     * Fixed issue with no loggers available and "memory leak"
     * Added "firewall exception" to installer
     * Fixed an issue with the socket data buffer
     * Added new option to NSC.ini [NSCA] socket_timeout=30 (timeout in seconds when reading from NSCA sockets)
     * Fixed issue with NSCA socket.
    
    2009-07-05 MickeM
     * Fixed issue with CheckExternalScripts and script_dir: not adding the commands properly.
     * Fixed issue with CheckExternalScripts and script_dir: not using relative paths (#310).
    
    2009-06-20 MickeM
     * Fixed issue with CheckDisk and paths not working out properly
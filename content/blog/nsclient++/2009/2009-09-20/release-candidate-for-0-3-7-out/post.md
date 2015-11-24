Title: Release candidate for 0.3.7 out
Author: mickem
Tags: 0.3.7, release-candidate
Status: published

A new version (release candidate) for the next minor release is out.
Nothing major in this version mainly installer work as well as some
bugfixes.

     2009-09-20 MickeM * Fixed alias in CheckWMI (now works) + Added columnSyntax to CheckWMI to allow formating of returned data (default is %column%=%value%) + Added columnSeparator to CheckWMI to allow formating of returned data (default is ", ") 2009-09-13 MickeM * Fixed some more issues with the installer should not "work" on Windows 2008 as well as slightly simpler to configure. 2009-09-06 MickeM + Added new option to [NSCA Agent] string_length= of the NSCA_MAX_PLUGINOUTPUT_LENGTH option on the NSCA server. * Readded all the "installer configuration" crap which I accidentaly removed when I fixed the installer... *sigh* 2009-08-30 MickeM + Added -c and -d command line options like so: NSClient++ -c CheckFile2 path=c:test pattern=*.txt MaxCrit=1 filter+written=gt:2h NSClient++ -c    ... -d Is the same thing but with debug enabled. + Added uninstall of old client (sort of broken but works) 2009-08-29 MickeM * Fixed issue with CheckFile (directory) * Rewrote the CA:s in the installer to work "better" (hopefully) in general it should be have more like a propper installer. 2009-07-18 MickeM * Fixed issue with no loggers avalible and "memory leak" * Added "firewall exception" to installer * Fixed an issue with the socket data buffer * Added new option to NSC.ini [NSCA] socket_timeout=30 (timeout in seconds when reading from NSCA sockets) * Fixed issue with NSCA socket. 2009-07-05 MickeM * Fixed issue with CheckExternalScripts and script_dir: not adding the commands properly. * Fixed issue with CheckExternalScripts and script_dir: not using relative paths (#310). 2009-06-20 MickeM * Fixed issue with CheckDisk and paths not working out properly 

// Michael Medin

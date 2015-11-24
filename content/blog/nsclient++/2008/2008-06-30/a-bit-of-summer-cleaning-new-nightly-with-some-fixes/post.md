Title: A bit of summer cleaning (new nightly with some fixes).
Author: mickem
Status: published

I have closed a bunch of issues and gone through them and fixed some of
them. I shall see if I cant do the same tomorrow and then release the
long overdue 0.3.3. If you have an issue you want fixed in that release
get in touch with me tomorrow and I shall see what I can do. (I am
mainly looking at fixing various 64-bit/installer issues for tomorrow so
if there is anything else let me know)

     2008-07-01 MickeM + Added new option (namespace) to CheckWMI and CheckWMIValue use like so: CheckWMI namespace=rootcimv2 MaxCrit=3 MinWarn=1 "Query:load=Select * from win32_Processor" 2008-06-30 MickeM * Fixed issue with CheckFile and performance data ( #156 ) + Added option (InvalidStatus) to CheckCounter to allow other then UNKNOWN return state when counters are missing ( #167 ). *NOTICE* this is all reasons (so if the counter is missing or some such the same will happen not just when the instance is missing) Message will reflect reason. * Fixed issue in the arraybuffer (one of the split functions had a problem with multiple chars of the same) ( #190 ) 

The nightly is named: NSClient++-Win32-20080701 to download click the
"Download" tab above. // MickeM

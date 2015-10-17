Title: 0.4.2 RC3 (0.4.2.66)
Author: mickem
Tags: 0.4.2, release-candidate
Status: published

Hello Yahoo search bot!

Another week another release candidate.

This time I hope all CheckSystem commands should work in compatibility
mode. There is one important snag currently which is that multiple
warn/crit thresholds are now silently ignored. This is due to a shift in
how the newer version works.

Before NSClient++ had a position based argument system which means that
order mattered as this was confusing the newer commands instead have a
key-based argument system meaning two arguments of things that does not
stack is not possible.

I have also added some really nice features chief among them is the new
lua script check\_cpu\_ex which provide top consumers in the check\_cpu
command.

I have also added %() for all expressions (before \${}) to make escaping
simpler in Nagios.

You can find the latest RC if you click the
<http://nsclient.org/nscp/downloads>  in the top right corner! **Look
for 0.4.2.66**

// Michael Medin

**Full changelog:**

     2013-12-05 MickeM - RC3
     * Added suport for instances (new keyword instances) to check_pdh
     * Fixed more compatiblity issues 
    2013-12-04 MickeM
     * Added check_cpu_ex.lua script to return top consumers for check_cpu command.
     * Harmonized the compatiblity layer so all commands "work the same" 
    2013-12-03 MickeM
     * Added new command: filter_perf to filter the returned performance data
     * Fixed some issues (API changes) in Lua script module 
    2013-11-29 MickeM
     * Fixed issue with logger 
    2013-11-28 MickeM
     * Added %() for all expressions to make esacping in nagios simpler.
     * Fixed crash in check_nscp * CheckDriveSize (compatiblity) fixed support for multiple bounds will only use "one of them" though.
     * Fixed some regression issues for check_nt (disk, memory uptime, services)
     * Added $ARGS$ to CheckExternalScript to add scripts with variable argument lists
     * Added $ARGS"$ to CheckExternalScript to add scripts with qouted variable argument lists 
    2013-11-27 MickeM
     * Fixed _user arguments for check:drivesize (which can be used for drives with qouta) 
    2013-11-26 MickeM
     * Improved compatiblity for CheckDriveSize
     * Added total (option) to check_drive to get/check the total size of all (matching) drives
     * Fixed bounds calculation for check_drivesize
     * Fixed issue with the show-all flag beeing on by default.
     * Fixed issue with converting to byte units for very large/small numbers

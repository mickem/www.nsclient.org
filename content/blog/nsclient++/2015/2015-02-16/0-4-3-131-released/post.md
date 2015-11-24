Title: 0.4.3.131 released
Author: mickem
Tags: 0.4.3, github, release, updates
Status: published

A new build of NSClient++ has been released.\
 It is mainly a bug fixes release and fixes most known issues which has
surfaced in the last few weeks.\
 For those who do not know we have switched to using github for tickets
which has been a huge success. I will be deprecating sourceforge hence
forth mainly as it is a pain to work with their rather inflexible API:s.

> As someone mentioned a while back\
>  "sourceforge: github for old people"

So I have started to extend the github integration and am now using
their release modules for hosting files. You can always find the files
here as well but some thins like symbols and what not will be simpler to
get from github.

Now to get back to build 131 your probably wondering whats new right?\
 And the answer is a lot but I would say the most interesting bit is all
the pull-requests I have received on github, a massive thank you!!! to
everyone who has helped out:

-   Andrew Widdersheim
-   Cybervitexus
-   Milan Dadok
-   Bruno Bigras

<!-- -->

    New features:
     * #91 Added new command xform_perf which can transform performance data (currently only supports extracting maximum/minimum from int/float values)
     * Added new utility function render_perf to render performance data in the message.

    Enhancements:
     * #110 Added support for using units in check_cpu
     * added error handling for invalid states on checkservice
     * #103 Improved error messages and logging related to settings
     * improved error handling is service check parsing failes
     * Added support for arrays and rendering invalid columns
     * Fixed some inconsistencies with the installer NRPE configurator
     * Fixed some issues with nrpe installer and ssl options
     * #94 Fixed so log file is reverted to real default is the wrong one is used.
     * #91 Added documentation about perf-config (Updated docs)
     * Fixed selector filtering so all names are trimmed for spaces.
     * Changed so perf config selectors use dot notation instead of no notation.
     * Added support for parsing expressions with '' in performance config as well as . and some such in the keywords
     * Added new option to all commands show-default to show the default command line used when a command is invoked.
     * Perfdata units (and others) are no longer case sensitive
     * Implemented empty syntax as a proper syntax string (i.e replacement variables)
     * Added support for empty-state (should work now)
     * Implemented ok-syntax in most checks to make the ok message a bit nicer...
     * flags property of PDH counter can be specified as check_pdh argumnet, but not in INI
     * PDH counter with rrd buffer will return oldest value from buffer as current/actual value
     * Cannot add second PDH counter to INI

    Fixed bugs:
     * #105 Fixed issue with parsing legacy style checkservice comamnds
     * #102 fixed check_os_version default filter
     * #100 Fixed check_pdh not picking up warn short hand options.
     * Fixed crash upload configuration
     * Fixed check_process issues
     * Fixed all check_always_xxx commands so they work again...
     * #81 Fixed so check_wmi will work without warn/crit and changed so default formatting displayes all rows
     * #98 Fixed so ok syntax is not used if you have customized the regular output to contain all data
     * #96 Fixed pagefile size block conversion using the actual architecture value
     * #49 Fixed issue with rounding performance data
     * #94 Fixed default log file location
     * #83 Fixed issue with invalid packet type (the default for extended response is now disabled in "insecure mode")
     * Improved error message for ssl errors (which are now likely due to the insecure option)
     * #92 Fixed so triggered services are ignored.
     * Added trigger start support (for real this time, honest... i promise!!!)
     * #78 removed the delayed() from ok message
     * Return result from check_nrpe

    General improvements:
     * Fixed compiler warning
     * Tweaked build a bit to resuse some code
     * added postbuild.bat to work around using the wrong python.exe
     * Fixed so specified python is found before path python (i.e 32-bit python on 64 bit machines)
     * Added option to rebuild without bumping version
     * Changed symbol paths
     * bumped versions and updated docs
     * Fixed crash upload properties to work with new collector
     * Added support for creating github releases
     * Added documentation for chiper strings
     * Fixed some issues with crash reporter
     * Fixed crashdump folder
     * tried to fix floating point plattforma independent issues a but ugly...
     * Added test cases for rounding performance data
     * refactored fetch delayed into a function
     * Fixed missing return statement
     * Fixed compiler warning about unused variable
     * Fixed unix checks to work with new arguments
     * Fix typo in create_plugin_module.py
     * removed --format from docs.py since there is only one format


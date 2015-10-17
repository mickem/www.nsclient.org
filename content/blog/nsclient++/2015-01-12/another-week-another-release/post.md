Title: Another week another release
Author: mickem
Status: published

Last week's buzz was all about the new 0.4.3 and this week we will
spread the buzz to include the slightly older 0.4.2 as well.

The hightlights from 0.4.3 is bug fixes and some security enhancements.
On popular request you can now disable sslv2 and sslv3 so you can make
your security scanners happy. This is the default in "safe mode" (i.e.
non legacy ssl). For other fixes please check the changlog.

Please note this is a work in progress, so linux and docs will be
updated later today...

    2015-01-11 Michael Medin
     * Added new options to disable sslv2 and sslv3 (enabled by default in secure/safe mode)

    2015-01-07 Michael Medin
     * #74 Fixed check_process empty list returns ok status
     * #72 Fixed issue with rate counters not working.
     * #75 Fixed so modules have a version block
     * Fixed so version use . not ,
     * #75 Fixed error reporter information and improved the icon
     * #75 Changed icon name to something more sensible

    2015-01-06 Michael Medin
     * #73 set legacy performance data suffix to empty.
     * Added option to set suffix/prefixes to empty using perf-config.
     check_pdh ... perf-config=*(suffix:none)
     * Fixed missing sample from documentation
     * Use the same name/desc for password (common key)

When it comes to 0.4.2 it has received some love in the form of getting
some of the recent 0.4.3 fixes as well as the (what I believe to be a
false positive) virus alert has been removed in the form of a new build
with a new signature.

    2015-01-08 - Michael Medin
     * fixed settings refactoring issues
     * bumped openssl version to k (j does not build?)
     * Fixed service dependency
     * Fixes CheckEventLog error handling if EvtQuery fails
     * #47 Fixed so totals are caluclated correctly when drives are not in the filter
     * #45 Fixed missing %total% conversion in check_files
     * #43 improved error message when English counters fails.
     * Fixed no global version.hpp
     * #67 Fixed command line missing from check_process
     * #74 Fixed check_process empty list returns ok status
     * #75 Changed icon name to something more sensible
     * improved help and removed json generation (not really used)
     * fixed build script
     * #75 Fixed error reporter information and improved the icon
     * Something with the docs?
     * #75 Fixed so modules have a version block
     * Fixed so version use . not ,
     * Fixed buffer overflow in external scripts
     * moved my local build folder (should probably make this an argument or some such :)
     fixed some issues in the batch builder
     * Fixed #730 check_tasksched / most_recent_run_time not working
     * added google test

Title: New NSClient++ RC/build 0.4.3.142
Author: mickem
Tags: 0.4.3, release-candidate, updates
Status: published

Greetings bing search spider!

Since I have done some infrastructure changes (newer version of
components) I figured I would do a release candidate for the next 0.4.3
update. Apart from infrastructure changes this also contains some
bugfixes as well as new features.\
 If no issues are reported in the next few days I will release this
as-is.

So whats new?

-   Bug fixes to check\_drivesize, check\_files check\_page as well as
    others
-   New module CheckNet and command check\_ping which will replace the
    check\_ping.bat script eventually (this is hightl experimental as of
    yet so use with care)
-   Simplified the crash reporter so you can now do: reporter.exe send
    b1438ab2-20a3-4b2d-bc30-7c3033c084e1.dmp

<!--more-->

\[su\_row\]\
 \[su\_column size="1/3"\]\
 \[su\_button
url="http://www.nsclient.org/files/nightly/NSCP-0.4.3.142-x64.msi"
background="\#45a43a" wide="no" center="yes" icon="icon:
download"\]Windows 64bit\[/su\_button\]\
 \[/su\_column\]\
 \[su\_column size="1/3"\]\
 \[su\_button
url="http://www.nsclient.org/files/nightly/NSCP-0.4.3.142-Win32.msi"
background="\#45a43a" wide="no" center="yes" icon="icon:
download"\]Windows 32bit\[/su\_button\]\
 \[/su\_column\]\
 \[su\_column size="1/3"\]\
 \[su\_button
url="http://www.nsclient.org/files/nightly/NSCP-0.4.3.142-1.x86\_64.rpm"
background="\#45a43a" wide="no" center="yes" icon="icon:
download"\]Redhat/Centos 7 64bit\[/su\_button\]\
 \[/su\_column\]\
 \[/su\_row\]

Full changelog can be found here:

    2015-04-27 Michael Medin
     * Improved the logging around connection failures
     * Improved the reporter syntax:
       reporter.exe send b1438ab2-20a3-4b2d-bc30-7c3033c084e1.dmp

    2015-04-08 Michael Medin
     * #139 Added support for showing file dates in local time (not just UTC)
     * Added check_ping command and CheckNet module
     * Fixed a few potential crashes with check_nt

    2015-03-24 Michael Medin
     * #123 fixed CheckAllOthers
     * #124 Fixed problem count variable
     * #131 Added support for service= to check_service
     * A lot of infrastructure changes and build fixes

    2015-02-23 Michael Medin
     * Fixed check_files empty  message to say files not drives.
     * #114 Fixed issue with empty-state which was ignored
     * A lot of infrastructure changes and build fixes

    2015-02-14 Michael Medin
     * Fix incorrect variable in check_page_filter()
     * Add pct to check_pagefile
       This is basically a clone of f90ab0bf which added pct to check_memory.

Or download other associated files from here:\
 \[fileaway type="table" base="5" only="0.4.3.65" exclude="md5"
heading="0.4.3" sortfirst="mod-desc"\]

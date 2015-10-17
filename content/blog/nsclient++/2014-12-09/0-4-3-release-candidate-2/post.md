Title: 0.4.3 release candidate 2
Author: mickem
Tags: 0.4.3, release, release-candidate
Status: published

Greetings yandex search bot!

A new week a new RC. Last week I release RC1 which included the first
ever Linux package.\
 This week I will spend some time on the windows side, I will hence
forth almost always release everything side-by side so whenever there is
a new windows build there will be new Linux builds as well (and vice
versa).

So whats new?\
 Since Rc1 last week, mainly bug fixes and a bunch of Linux fixes:

-   We can now build deb packages
-   Fixed how total is handled in queries
-   Fixed units in check\_memory (and checkmem)
-   Fixed some counter issues and improved error henadling a bit
-   Linux packages and installation fixes

But if you ask me the best thing is that through the magic of github
there is **three names in the changelog**!

**Massive thanks** to: **Pall Sigurdsson** and **Ben Brian** for
submitting pull requests!

<!--more-->

\[su\_row\]\
 \[su\_column size="1/3"\]\
 \[su\_button
url="http://www.nsclient.org/files/beta/NSCP-0.4.3.65-x64.msi"
background="\#45a43a" wide="no" center="yes" icon="icon:
download"\]Windows 64bit\[/su\_button\]\
 \[/su\_column\]\
 \[su\_column size="1/3"\]\
 \[su\_button
url="http://www.nsclient.org/files/beta/NSCP-0.4.3.65-Win32.msi"
background="\#45a43a" wide="no" center="yes" icon="icon:
download"\]Windows 32bit\[/su\_button\]\
 \[/su\_column\]\
 \[su\_column size="1/3"\]\
 \[su\_button
url="http://www.nsclient.org/files/beta/NSCP-0.4.3.65-1.x86\_64.rpm"
background="\#45a43a" wide="no" center="yes" icon="icon:
download"\]Redhat/Centos 7 64bit\[/su\_button\]\
 \[/su\_column\]\
 \[/su\_row\]

Full changelog can be found here:

    2014-12-08 Michael Medin
     * Fixed debian init script
     * Fixed version bump script
     * Improved debian packages
     * Added init.d init script (which seems to not work BTW)
    2014-12-07 Michael Medin
     * Tinkered a bit with process elevation tokens
     * added new field error to show any error messages associated with check_process
     * removed some travis deps no longer required (I think)
     * removed TODO return message from py scripts
     * updated docs
     * Fixed some restructured syntax bugs
    2014-12-06 Michael Medin
     * updated docs
     * Some linux package improvments
     * Added support of validating counters (and loading other counters if validation fails of a single one)
     * #43 improved error message when English counters fails.
    2014-12-05 Michael Medin
     * #45 Fixed missing %total% conversion in check_files
    2014-12-04 Michael Medin
     * #47 Fixed so totals are caluclated correctly when drives are not in the filter
     * #47 Fixed so total is not affected by filtering
     * Moved function to parse arguments into a shared function
     * #59 Fixed so check_memory (both unix/win) supports both % and KMBG units.
       i.e. check_memory "warn=used>30M" now works
    2014-12-03 Michael Medin
     * #60 Fixed no response for unknown file extensions in web server
     * Whoops, wrong syntax in spec file
     * Cleaned up web install output a bit #58
     * added self signed cert generation to spec file
     * Added command line interface to generate the self signed certificates: nscp nrpe make cert
     * Fixed so self signed certificates are not CA certs....
     * Merge pull request #29 from historicbruno/evtquery-error-fix
     * Merge branch 'master' of https://github.com/mickem/nscp
     * Fixed threading issue in registry (which was single threaded by proxy before)
     * Merge pull request #57 from palli/fix-typo-critcal
    2014-12-02 Pall Sigurdsson
     * Fix typo CRITCAL > CRITICAL
    2014-09-04 Ben Brian
     * Fixes CheckEventLog error handling if EvtQuery fails

Or download other associated files from here:\
 \[fileaway type="table" base="5" only="0.4.3.65" exclude="md5"
heading="0.4.3" sortfirst="mod-desc"\]

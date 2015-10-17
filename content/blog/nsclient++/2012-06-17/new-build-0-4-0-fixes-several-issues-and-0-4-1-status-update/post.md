Title: New build 0.4.0 fixes several issues and 0.4.1 status update...
Author: mickem
Tags: 0.4.0, 0.4.1, updates
Status: published

Hello, I have created a new build (176) of 0.4.0 it can be found under
nightly builds in the download section. Please give it a twirl as I will
update the official 0.4.0 in a day or so. == 0.4.0 == The main
highlights are bugs fixes (as is the intent with 0.4.0 hence forth). New
features are in 0.4.1. \* Reading commands from config file should now
work better \* Log can be disabled. \* "Fixes" for log getting spammed
by PDH error "negative denominator". For a fix see ticket \#436 which
has a reg patch which sopousedly fixes this which is due to a hypervisor
bug or so they say. \* Fixed performance data parsing See change log for
full details. == 0.4.1 == 0.4.1 also has a build out with a new one
coming in the next few days or so. The highlights from the 0.4.1
enhancements are: \* NRDP support (very early concept) \* Huge
improvement to real-time eventlog checking. \* Cleaned up almost all
-Wall warnings. \* New improved socket handling (less bugs) \* Initial
support for true ssl (early concept) \* Full (?) ipv6 support (including
host validation) Next up (for 0.4.1) are: \* Proper NRDP support \*
check\_mk support == Updates == And the big question: What would you
like to see added/fixed? Feel free to let me know! Also on my blog I
posted a question asking for ideas on what to say when I go to OSMC
(Yes, I will actually go this year, despite some previous rumors to the
contrary).
\[http://blog.medin.name/2012/06/14/what-would-you-like-to-hear-about/
Check it out here\]

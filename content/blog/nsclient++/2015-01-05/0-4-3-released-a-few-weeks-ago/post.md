Title: 0.4.3 Released (a few weeks ago)
Author: mickem
Tags: 0.4.3, icinga, naemon, nagios, nsclient, release, status
Status: published

### Yaaay!!!

After months of delays 0.4.3 was officially out during xmas. I always
release tings silently so early adopters can report back issues and bugs
before everyone installs things. So without further ado NSClient++ 0.4.3
(service release 2) is officially launched today!\
 This release fixes some issues as well as contains updated
documentation with a nifty whats new section.

So what is new you ask?

***Well, if you are on 0.4.2** not to much noticeable...*

![webui](/images/blog/webui-300x297.png) There
is a myriad of bug fixes and enhancements and what not, in general it is
a much cleaner version then pretty much all 0.4.x versions have been to
date. The goal of 0.4.3 was always to be a bug fixed version of 0.4.3.
But it does have one rather nice new feature which is the brand new WEB
UI. I really think this will help people work with NSClient++ as it
makes it much easier to navigate settings and queries and get online
help in real time. But all  in all your experience should be much
smoother with 0.4.3 as most parts have gotten some love.

***If you are on 0.4.1** (which has been the "stable" version up until
now) <span style="line-height: 1.5;">you are in for a treat!</span>*

<span style="line-height: 1.5;">There are many many many changes mostly
in how things work. It should be pretty compatible with the older
versions but all command have been reworked and the "filtering concept"
introduced in event log checks has been added to all checks. This means
you can now do a lot of cool stuff, but more importantly it means ALL
command work the SAME! Before most command had their own dialect and it
was a bit of guess work to figure out how a specific command and option
worked.</span>

<span style="line-height: 1.5;">The other major change introduced in
0.4.2 was that</span>**<span style="line-height: 1.5;">modern
windows</span>support**<span style="line-height: 1.5;">. Which means
NSClient++ should work much better checking Windows machines.</span>

**The biggest change** regardless of version you are on is **deprecated
insecure legacy NRPE**. This does not mean NRPE is dead instead it means
the legacy check\_nrpe with dubious SSL implementation is deprecated,
instead you can now use NSClient++ on both Linux and windows as a client
to get certificate based authentication on your NRPE connection.
Speaking of prtocols 0.4.3 has the first version of the REST support
which will become the preferred NRPE replacement in the next version.

> **You can during the installer opt to use the "insecure NRPE mode" if
> you want to remain compatible with the "old" check\_nrpe client.**

For a full list of changes please refer to the various documentation
pages which describes most major changes and of course the change-log
for the nitty gritty details.

-   [Changes in 0.4.3
    (from 0.4.2)](http://docs.nsclient.org/0.4.3/whatsnew/0.4.3.html)
-   [Changes in 0.4.2
    (from 0.4.1)](http://docs.nsclient.org/0.4.2/whatsnew/0.4.2.html)
-   [Change log
    (all changes)](https://github.com/mickem/nscp/blob/master/changelog)

### Download NSClient++ 0.4.3.77

\[su\_row\]\
 \[su\_column size="1/3"\]\
 \[su\_button url="/files/released/NSCP-0.4.3.77-x64.msi"
background="\#45a43a" wide="no" center="yes" icon="icon:
download"\]Windows 64bit\[/su\_button\]\
 \[/su\_column\]\
 \[su\_column size="1/3"\]\
 \[su\_button url="/files/released/NSCP-0.4.3.77-1.el7.x86\_64.rpm"
background="\#45a43a" wide="no" center="yes" icon="icon:
download"\]Redhat/Centos 7 64bit\[/su\_button\]\
 \[/su\_column\]\
 \[su\_column size="1/3"\]\
 \[su\_button url="/download/" background="\#4360d8" wide="no"
center="yes" icon="icon: download"\]Other options\[/su\_button\]\
 \[/su\_column\]\
 \[/su\_row\]

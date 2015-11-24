Title: 0.4.2 RC 1
Author: mickem
Status: published

Good news everyone! The first release candidate of 0.4.2 is out! This
new version (0.4.2) is a massive amount of new features and is the first
NSClient++ targeted at "modern windows". This means that all the old
checks have been rewritten to work flawlessly with all new Windows APIs
in newer Windows versions. In addition to this we have introduced the
filtering concept on almost all commands which gives you unlimited power
in turns of how to control your monitoring. To facilitate this we have
added a set of new commands with underscore in stead of camel case. So
to use the old check for cpu load you use CheckCPU and to use the new
one you instead use check\_cpu. When testing this new release candidate
it is very important to report back any bugs, especially, any "old
commands" which does not work. Last but not least there is a series of
blog posts which introduces this new version
\[\[http://www.nsclient.org/nscp/blog/category/0.4.2\]\] in addition to
this there is at last a brand new documentation site
\[\[http://docs.nsclient.org/\]\]. SO please try it out and let me know
how it works out! The plan is to add the Linux checks and then come with
an updated version (hopefully fixing any bugs) in about a week or so. //
Michael Medin

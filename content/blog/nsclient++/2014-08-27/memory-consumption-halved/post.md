Title: Memory consumption halved!
Author: mickem
Tags: 0.4.3, memory, nightly, status
Status: published

One of the major new but non-essential features of 0.4.3 is that it
supports dynamic linkage.

This means that for the first time the NSClient++ download size will
decrease instead of increase. This might not seem like a killer feature
and in truth it probably is not. But going forwards with NSClient++ it
will become ever more  important. With each new version we get more
modules and more features. this means that with each version we get more
code in each modules and more modules in the distribution. This means
that size is increasing exponentially.

Static linkage
--------------

So why do we use static linkage?

It is historical reasons: NSClient++ has always been linked statically.
This was excellent back in 2003 when you could download the exe file and
it just worked, No installer, no registration, no DLLs, no nothing. But
since then DLL hell has been resolved, and no one today use unzip to
install programs so the usefulness of static linkage has been sorely
outlived.

So whats the deal? Well changing linkage is a pretty big change since it
requires recompiling and re configuring all modules and what not. In
0.3.9 and previous everything was built by hand in 0.4.x I introduced
cmake to allow dynamically configure settings. But all support libraries
was still built by hand. In 0.4.2 I introduced the "fetchdeps" script
which helped build all dependencies (statically).

Download size
-------------

In 0.4.3 I have started to build most support libraries with NSClient++
and this makes it much simpler to change linkage on the fly. The biggest
change can be seen on the download page:

![static-download](/images/blog/static-download1.png)

The 64 bit version is the one which is dynamically linked and it is less
than half the size (22Mb) of the statically linked w32 version (38.6Mb).

RAM Size
--------

This size is not only visible on disk (where it expanded is much bigger
difference) it is also visible in run time memory.

[![static-memory](/images/blog/static-memory.png)

This is a screen grab from task manager showing 32 and 64 bit version
with ALL plugins loaded. This is not a normal scenario since most people
only use a handful of modules but still it shows the change
quite nicely. The red line represents the w32 version which is
statically linked and it use over 100Mb of RAM where as the x64 version
(green line) use less than half (and most of that is shared).

For those wanting to test out the new version I will tomorrow swap over
the w32 version to use dynamic linkage as well and clean up all "old"
versions which currently is a bit of a mess :)

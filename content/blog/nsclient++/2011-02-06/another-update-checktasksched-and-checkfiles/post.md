Title: Another update CheckTaskSched and CheckFiles
Author: mickem
Status: published

I just committed a monster (unified diff was around 10.000 lines) :P The
main highlights is: \* refactored filter framework to reduce compile
times a bit. \* New CheckFiles command using the "where syntax"
CheckFiles path=c:foo "filter=size &gt; 500k AND written &lt; 2d" ... \*
New CheckTaskSched command using the "where syntax" CheckTaskSched
"filter=status&running=running AND title != 'google'" ... \*
'''IMPORTANT''' CheckFile is '''REMOVED''' It has for quite some time
been deprecated in favor of the CheckFile2 which will be deprecated in
this release in favor of the much improved CheckFiles command. All of
this is a bit experimental still so syntax is subject to change (the one
in the example, but hopefully you will get the idea). Also since this is
a lot of new code I will need some time to test and work through it.
After that I might look into the "negative denominator" PDH issue or I
will release 0.3.9 (and start working on 0.4.x which is also close to
beta alfa stage). // Michael Medin

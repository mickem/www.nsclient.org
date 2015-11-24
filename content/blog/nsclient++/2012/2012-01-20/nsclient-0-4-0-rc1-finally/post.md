Title: NSClient++ 0.4.0 RC1! (Finally)
Author: mickem
Tags: 0.4.0, release, release-candidate
Status: published

'''build 126''', 127 will be out later tonight whith some fixes to NSCA
unit-tests. After years of vapor ware and many broken promises I can
finally proudly pressent the first release candidate of NSCLient++
0.4.0! So what can you expect you ask? Quite a lot in fact but currently
the rather sad answer will be unfortunetly "not much". Now this is a
good thing and the reason is that the idea is that anyone runnign on a
previous version of NSCLient++ should be able to just upgrade and not
notice the difference (except for the odd bug fix here and there). But
for all the rest of you who do not want to "just upgrade" there is a
massive amount of new features. The two biggest changes will undoubtedly
be the linux support as well as is a shift from beeing a "NRPE client"
to more of a monitoring gateway which supports more protocols (with even
more in the pipe). Another other major change is ofcourse the embedded
python interpreter and the very extensive python API making it possible
to create plugins in python which can have state across your monitoring.
So now it is just for everyone to go out test it and let me know what is
not working so we can release a bug free version in the near future. I
have not set a date as I am relaying on the community (yes, that is
you!) for doing much of the test work and that may or may not take a lot
of time (depending on how much YOU! test). Stability and quality wise I
hope it is farily stable and everything works as-is but one never knows
when there is such a massive update. Especially as it is apretty
free-form application which has a lot of the edge cases. But another
major improvment is that there are now unit-tests which test various
parts of the application at the time of writing there is around 1000
unit tests which more to come. == Many new protocols == We now support a
number of new protocols (as well as old). '''Currently supported:''' \*
NRPE \* NSCA \* "check\_nt" \* SysLog \* SMTP \* NSCP (early concept
version, both as distributed (think gearman) and non distributed (think
NSCA/NRPE)) '''In the works:''' \* http (rest) \* Graphite \* check\_mk
\* NRDP \* SNMP \* WMI \* "native remote windows checks" == Brand new
API == Major new API changes which allows a lot more flexibility as well
as extensible from modules and scripts. '''Currently supported:''' \*
Python \* plugins \* Lua (old API currently) '''In the works:''' \* Lua
\* .Net == Brand new settings sub systems == Brand new flexible settings
sub systems which supports many new formats as well as generation and
including cross formats. '''Currently supported:''' \* ini-files \*
registry \* http (ini files) \* old \* dummy (in memory store) '''In the
works:''' \* XML \* improved http == Other fixes and enhancments == We
have of course a myrriad of bug fixes enhancments and and such here are
a few highlights. '''highlights:''' \* Brand new (easy to use?) command
line interface \* Linux suppport (as mentioned previously) \*
CheckProcState: Enchancements \* CheckEventLog: Real time checking \*
CheckWMI: Remote check support (rather crude currently) \* lots of other
things but focus is mainly on internals so checks are mainly the same
'''So! Test away, and hit me with your bugs, defects, problems, and
issues...''' // Michael Medin

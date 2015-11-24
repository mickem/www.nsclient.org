Title: New w32 nightly up!
Author: mickem
Status: published

Would be interesting to get some feedback on this. Since there is still
a lot of issues with the locale and PDH I have decided to make a 3.1
release "soon" that will fix this (have been in the nightly a while
now). ANd while I am at it I will add the following new features: \*
NSCA support \* LUA Script support \* Enhancements to the eventlog
check. \* Improved SysTray functions and dialog. The NSCA support is for
thos who want to use passive checks only (using this nagios-server you
can have the client "phone home" with results instead of nagios asking
all the time). LUA scripts is for those who want to have a bit more
control, there you can write and modify your own checks "inside" NSCP
without the need for external script, don't know how interesting it is
but it is there. The use-case that brought this on was: "I don't want
the demon to do X can you change this?" With a LUA script '''you''' can
change it :) Enhancements to the event log check (and keep coming up
with more ideas) \* A unique filter (only return 1 log entry for each
problem-kind. \* Fixed "time-zone" issues (entry are now returned in the
proper local time and not UTC) \* New %message% format option to display
the \*proper\* eventlog message instead of the previous crap :)
Enhancements to the SysTray dialog are numerous: the dialog has been
reworked and an API to list/describe commands have been implemented. I
would really like to get some feedback on the new modules as well as the
new eventlog check., I will try to finalize some issues and have a
release out by the end of February or so. // MickeM

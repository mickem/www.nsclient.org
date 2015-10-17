Title: 0.4.1 RC4 (Last change to report bugs)
Author: mickem
Tags: git, release-candidate
Status: published

Hello, release RC4 of 0.4.1 (build 72). It contains some fixes for major
issues and hopefully the last batch. Since I have promised to release
0.4.1 this year I hope this will be the final RC so unless there are no
important issues this will become golden (ie. release) in a week or
so... So please pleas please everyone try it out and let me know any
issues you have! Change log:

     2012-12-02 MickeM * Added option to disable new alias check_cpu and only register old ones CheckCPU [/settings/default] modern commands=false 2012-11-29 MickeM * Improved exception handling in server threads 2012-11-28 MickeM * Fixed crash in NRPE server when payload was to large (#585 #582) * Fixed issue with lua unit test * Added payload length simulation in lua unit tests (so it returns various payload sizes) * Added nscp.sleep to Lua scripts (but dont use as I will implement coroutines in 0.4.2) * Fixed registry settings bug * Fixed issue with parsin performance data with leading spaces * Fixed issue with rendering filters 

Also I have switched master to 0.4.2 so master is now development
branch. 0.4.1 remains in 0.4.1 branch, and previous master is now 0.4.0
(which contains the 0.4.0 code). // Michael Medin

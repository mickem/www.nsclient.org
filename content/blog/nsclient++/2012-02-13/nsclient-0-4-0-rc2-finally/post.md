Title: NSClient++ 0.4.0 RC2! (Finally)
Author: mickem
Tags: 0.4.0, release, release-candidate
Status: published

RC2 out finally ('''Built 134''')!. This is again long over due mainly
as the target re factoring took 2 more weeks than anticipated. Well it
is not really out it is building currently and I am an optimist assuming
it will build ok meaning in a bit you can find 134 under nightly and
tomorrow morning you can find it under RCs. The main highlights are
fixes with loading "objects" (targets and schedules) which now works
much more smoothly and you now also get documentation in your settings
file as well. The other main high light is a new improved Lua API
meaning you can now utilize the same (almost) features as the Python
scripts can do from Lua. The only thing lacking currently is protocol
buffer support. But protobuf support for Lua will not make it into 0.4.0
as I am unsure how to do that since there is no native Lua library for
protobuf. Other notable fixes are: \* The broken installer is now fixed
\* Ability to target scheduled tasks easily \* A lot more unit tests \*
Bug fixes here and there

     2012-02-13 MickeM * Fixed installer issue (could not start service) 2012-02-12 MickeM * Added support for specifying targets on schedules: [/settings/scheduler/schedules/foo] target = foo-host Will re-target the NSCA (or whatever you use) towards a given target. * Fixed is schedule manager uses new standard object reader * Fixed some issues with reading schedule 2012-02-05 MickeM * Added test cases for targets to NRPE * Added test cases for targets to NSCA * Added test cases for lenghts to NSCA * Changed to python API sleep uses milliseconds (not seconds as before) Makes NSCA unittests go much faster (as I can wait much less) * Fixed a lot of bugs related to target handling. * implemented target refactoring on all Client modules. 2012-02-05 MickeM * Refactored the targets concept internally to be simpler to use (less code) * Fixed issue with reloading plugins * Fixed target handling in NRPE Client, will add NSCA client tomorrow... 2012-02-02 MickeM * Implemented full API for LuaScript Now "everything" (ish) works including channels, exec and query (via moderna API) Still no protocol buffer support but not sure how to play that yet so will not be avalible in 0.4.0. 2012-02-01 MickeM * Implemented full settings API for LuaScript (next RC will have to wait till next weekend) 2012-01-31 MickeM1 * Fixed issue with parsing "invalid external commands". If parsing falies it will notify you but use the legacy split string method instead. * LuaScript module is now modern (ie. works with 0.4.0) Should be 99% compatbile (function needs to be defined before registration) but all old scripts should work now (I think) * LuaScript module has been modernized The new API is very similar to Python Concepts are working but not all commands have beenh implementes (and no testcases either) The old API will still work * Fixed issue with 2012-01-27 MickeM * Changed CheckCounter format option to take a coma separated list of keyword from the below list: nocap100: Counter values above 100 (for example, counter values measuring the processor load on multiprocessor computers) will not be reset to 100. The default behavior is that counter values are capped at a value of 100. 1000: Multiply the actual value by 1000. noscale: Do not apply the default scaling factor. So format=nocap100,noscale would combine the two aspects above. 2012-01-26 MickeM * Fixed issue with parsing multiple performance data items (internally) * Added option to CheckCounter format=nocap100 to not cap counters at 100% (for multi cpu machines) 2012-01-22 MickeM * Fixed help when specifying invalid options on command line * Eradicated a potential memoryleakin the NSCA encryption library 

Title: New w32/x64 build!
Author: mickem
Status: published

Hello, a new build (and hopefully the last before I start doing RC:s
next week) '''Whats new?''' \*A lot\* (internally) I have changed to a
unicode build so virtuall \*all\* string handling have been tinkerd with
so things might be broken, but it seems to work, so lets hop it is all
good. I have also added a long awaited feature: you can now escape
strings with ":s in the nclient++ /test mode but that is not so usefull
actually, just for me when I do testing of WMI stuff :) If things work
as nicely on vista/2k3/x64 I shall come up with a itanium build and
start doing RC (Release Candidates) for the 0.3.0 version early next
week. Also done some changes to the page so hopefully it shall be
slightly esier toi navigate (as the "tabs" were starting to fill up) //
MickeM

     2007-11-23 MickeM * Converted to unicode (damn sometimes I **HATE** C++) + Added support for escaping " on the /test syntax so now you can do: CheckWMI MaxCrit=3 "MinWarn=1" "Query:load=Select * from win32_Processor" 2007-11-22 MickeM * Fixed so the "default path" is correct even when running as a service (issue: #96) 2007-11-21 MickeM * Fixed process counter so checkProcState now return the *correct* number (previously it was correct-1) * Fixed som missing exceptions that were not caught + Added "AliasCol" option to CheckWMIValue to allow a column to be used as "alias" for a result set: CheckWMIValue -a "Query=select Caption, ThreadCount from Win32_Process" MaxWarn=50 MaxCrit=100 Check:threads=ThreadCount AliasCol=Caption will give you: "System threads: 98 > warning, svchost.exe threads: 87 > warning" - Removed documenation from SVN (as it is old and outdated and no longer used) 2007-11-20 MickeM + Added new option to CheckSystem to override detected language (force_language=0x0014) 

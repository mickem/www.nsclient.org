Title: New nightly 0.4.0 build as well some som information on distributed monitoring
Author: mickem
Tags: 0.4.0, release-candidate
Status: published

First off Linux seems to be doing great most features just works and
thus far I am pretty impressed with the "portability". I have written a
page on how to build on Linux if you want to try it out for your self
\[wiki:build/04x/linux\]. The new nightly has a lot of new features as
well an updated installer with I hope works better. If you have upgraded
previously from 0.3.9 I would recommend downgrading/upgrading again as
you will most likely have a broken setup. (or you can just upgrade again
removing any boot.ini / nsclient.ini fille you may have). Main highlight
is the PythonModule which now supports many advanced features of
NSClient++ (see the included script) as well as some new remote WMI
stuff. As I have said before (I hope) one of the main new features of
0.4.x is the distribution so I have started to implement that now and
one step there is the new remote WMI checking thingy. The new remote
checking features works like this. First you configure a remote host:

     [/settings/targets] my_test_xp_vm= [/settings/targets/my_test_xp_vm] hostname=192.168.0.123 username=foobar password=foobar protocol=none 

Then the idea is that you can run checks on "this host" which will
transparently be transported to the other host. Now since NRPE does not
support this (natively) we have to fake this using an argument like so:

     CheckWMI target=my_test_xp MaxCrit=3 MinWarn=1 "Query:load=Select * from win32_Processor" 

But the idea is that in the future you can just do:

     nscp_client --target my_test_xp --command CheckWMI ... 

And this will happen magically using the internal routing (regardless of
how nsclient++ needs to do it). For instance the idea is that the
following should be "magically":

      -{NRPE}->  -{SSH}->  -{NSCP}->  -{WMI}->  

But this is pretty far down the line so dont expect anything next few
days :P // Michael Medin

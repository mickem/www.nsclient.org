Title: 0.4.0 build 93 out and how to play with Python: NSClient++ style!
Author: mickem
Tags: 0.4.0, linux, python, test
Status: published

Hello again dearest Google bot! Today I have a pretty big announcement
for all you 0.4.0 waiters out there. I have release another nightly
build which is the result of a lot of work put in during august. The
main new features is of course the new protocol as well as a very
extended PythonScript module. Since there is so much new it is a bit
difficult to create s short blog post to summarize the new features. But
I hope that the new test.py and test\_pb.py scripts will eventually
cover most of the features if nothing else as a test script. ==
Installing Scripts == The best way to get start with these scripts are
to "install them". Something which is now supported from the command
line lik so:

     nscp --client --module PythonScript --command execute-and-load-python --script test.py 

This is a pretty complicated command actually. The first thing we do is
add '''--client''' which runs command line queries as well as commands
on modules without launching NSClient++ in server mode. IN essence this
is the "offline mode". Then we have '''--module PythonScript''' which
tells the "client" to load the PythonScript module (regardless of what
your configuration says) this also prevents any configured modules from
being loaded. The next step is the '''--command
execute-and-load-python''' which actually just sends a command down the
pipeline to see if any plugin want to run it. In this case the
PythonScript module will run it and do so by executing the '''---script
test.py''' script. This script is then the magic, if we look at the
\_\_main\_\_ function of this script we can see the following:

     def install_test(arguments): log('-+---==(TEST INSTALLER)==---------------------------------------------------+-') log(' | Setup nessecary configuration for running test |') log(' | This includes: Loading the PythonScript module at startup |') #... log('-+--------------------------------------------------------==(DAS ENDE!)==---+-') conf = Settings.get() conf.set_string('/modules', 'pytest', 'PythonScript') conf.set_string('/settings/pytest/scripts', 'pytest', 'test.py') conf.save() def __main__(): install_test([]) 

The interesting thing here is that we have a python script which is
modifying our configuration by first enabling the PythonScript module
(using an alias: pytest) and then adds the relevant script (again with
an alias pytest). The reason for using the alias is so we can easily
"uninstall" this without messing up your configuration. This is thanks
to the new fully supported multiple module support. Now unfortunately
NSClient++ does not (yet) support uninstalling but that will come. The
next step is (as the install command above will tell you) to reun the
test script from the "test mode". == Test mode == Test mode is nothing
new since as far as I can remember it has been possible to run
NSClient++ is "test mode" previously we used -test and for 0.4.0 we use

     nscp --test 

This will start NSClient++ like a service with three main exceptions: 1.
The program will run with '''YOUR''' privileges and in '''YOUR'''
session (not system) 2. The program will run with console log and debug
log enabled 3. You will be able to interact with NSClient++ directly So
lets try it out.

     D:sourcenscpbuildx64>nscp --test l ......trunkserviceNSClient++.cpp:536 NSClient++ 0,4,0,93 2011-09-04 x64 booting... d ttings_managersettings_manager_impl.cpp:148 Boot.ini found in: D:/source/nscp/build/x64//boot.ini d ttings_managersettings_manager_impl.cpp:165 Boot order: ini://${shared-path}/nsclient.ini, old://${exe-path}/nsc.ini d ttings_managersettings_manager_impl.cpp:168 Activating: ini://${shared-path}/nsclient.ini d ttings_managersettings_manager_impl.cpp:68 Creating instance for: ini://${shared-path}//nsclient.ini d trunkincludesettings/settings_ini.hpp:256 Reading INI settings from: D:/source/nscp/build/x64//nsclient.ini d trunkincludesettings/settings_ini.hpp:230 Loading: D:/source/nscp/build/x64//nsclient.ini from ini://${shared-path}/nsclient.ini l ......trunkserviceNSClient++.cpp:541 Booted settings subsystem... d ......trunkserviceNSClient++.cpp:602 On crash: restart: NSClientpp d ......trunkserviceNSClient++.cpp:614 Archiving crash dumps in: D:/source/nscp/build/x64//crash-dumps d ......trunkserviceNSClient++.cpp:681 booting::loading plugins d ......trunkserviceNSClient++.cpp:389 Found: PythonScript as pytest d ......trunkserviceNSClient++.cpp:689 Processing plugin: PythonScript.dll as pytest d ......trunkserviceNSClient++.cpp:926 addPlugin(D:/source/nscp/build/x64//modules/PythonScript.dll as pytest) d ......trunkserviceNSClient++.cpp:902 Loading plugin: PythonScript as pytest d nkmodulesPythonScriptPythoDn:S/csroiuprtc.ec/pnps:c1p5/6b u iLloda/dxE6x4 /isnc rPiyptthso/npSyctrhiopnt/ taess tp.yptye st d nkmodulesPythonScriptPythonScript.cpp:213 Looking for: test.py d nkmodulesPythonScriptPythonScript.cpp:213 Looking for: D:/source/nscp/build/x64/scripts/python/test.py d nkmodulesPythonScriptPythonScript.cpp:259 Adding script: pytest (D:/source/nscp/build/x64/scripts/python/test.py) d nkmodulesPythonScriptPythonScript.cpp:106 Loading python script: D:/source/nscp/build/x64/scripts/python/test.py e modulesPythonScriptscript_wrapper.cpp:15 Testing to register a function d ......trunkserviceNSClient++.cpp:714 NSClient++ - 0,4,0,93 2011-09-04 Started! l rcenscptrunkservicesimple_client.hpp:30 Enter command to inject or exit to terminate... 

So now we are all set. The next step is to run the commands command
which will list all available commands:

     commands l rcenscptrunkservicesimple_client.hpp:12 Commands: l rcenscptrunkservicesimple_client.hpp:12 | pytest_test: Run python unittest 

Now this is a pretty slim set of commands as I am only loading my script
and my module. Normally you will have a lot more commands here. But lets
run the command and see what happens:

     pytest_test d ......trunkserviceNSClient++.cpp:1021 Injecting: pytest_test... d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_channel_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_channel_001: OK e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple ok d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_channel_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_channel_001: WARNING e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple warning d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_channel_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_channel_001: CRITICAL e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple critical d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_channel_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_channel_001: WARNING e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple unknown d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_channel_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_channel_001: OK e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple performance data 001 d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_channel_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_channel_001: OK e modulesPythonScriptscript_wrapper.cpp:15 FAILED - Test did not get the correct retuirn code: 'foo'=5% = 'foo'=5%;10 d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_channel_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_channel_001: OK e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple performance data 003 d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_channel_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_channel_001: OK e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple performance data 004 d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_channel_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_channel_001: OK e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple performance data 005 e modulesPythonScriptscript_wrapper.cpp:15 ERROR: 1 tests failed e modulesPythonScriptscript_wrapper.cpp:15 Tested Testing that channels work (1 of 9) d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_command_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_command_001: OK e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple check d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_command_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_command_001: OK e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple check: Ok d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_command_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_command_001: WARNING e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple check: Warn d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_command_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_command_001: WARNING e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple check: Unknown d ......trunkserviceNSClient++.cpp:1021 Injecting: _pytest_test_command_001... d ......trunkserviceNSClient++.cpp:1051 Result _pytest_test_command_001: CRITICAL e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple check: Crit e modulesPythonScriptscript_wrapper.cpp:15 OK: all tests successfull e modulesPythonScriptscript_wrapper.cpp:15 Tested Testing that channels work (0 of 9) d ......trunkserviceNSClient++.cpp:1051 Result pytest_test: CRITICAL l rcenscptrunkservicesimple_client.hpp:12 CRITICAL:Tests failed 1 of 18 

This is a big chunk of output and unfortunetly we get a lot of debug
output here as well, some day I shall improve this to list all relevant
output at the end. But the interesting tidbits (cleaned up below)

     pytest_test e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple ok e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple warning e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple critical e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple unknown e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple performance data 001 e modulesPythonScriptscript_wrapper.cpp:15 FAILED - Test did not get the correct retuirn code: 'foo'=5% = 'foo'=5%;10 e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple performance data 003 e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple performance data 004 e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple performance data 005 e modulesPythonScriptscript_wrapper.cpp:15 ERROR: 1 tests failed e modulesPythonScriptscript_wrapper.cpp:15 Tested Testing that channels work (1 of 9) e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple check e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple check: Ok e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple check: Warn e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple check: Unknown e modulesPythonScriptscript_wrapper.cpp:15 OK - Test successfull: simple check: Crit e modulesPythonScriptscript_wrapper.cpp:15 OK: all tests successfull e modulesPythonScriptscript_wrapper.cpp:15 Tested Testing that channels work (0 of 9) l rcenscptrunkservicesimple_client.hpp:12 CRITICAL:Tests failed 1 of 18 

And as we can see all tests but one succeeded and that is a but I shall
fix at some point. When you only have a warning threshold and no
critical threshold the warning one is discarded in the parser. Now the
cool thing is that this all work the same from linux... and with the
right setup and some tinkering... remotely... pretty cool huh? //
Michael Medin

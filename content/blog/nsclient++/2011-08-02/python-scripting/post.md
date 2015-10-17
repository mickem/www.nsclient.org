Title: Python scripting!
Author: mickem
Tags: python
Status: published

Hello just a quick status update. I have been working on the python
scripting module last few days and it is starting to come together now
so with a bit of luck it will be out in alfa early next week.. Currently
my test script looks like this:

     from NSCP import Settings, Functions, log log('Hello World') conf = Settings.get() val = conf.get_string('/modules', 'PythonScript', 'foo') log('Got it: %s'%val) def test(foox): log('inside proc: %s'%foox) log('Testing to register a function') fun = Functions.get() fun.register_simple('py', test, 'This is a sample command') log('Testing to register settings keys') conf.register_path('hello', 'PYTHON SETTINGS', 'THis is stuff for python') conf.register_key('hello', 'python', 'int', 'KEY', 'This is a key', '42') log('Testing to get key (nonexistant): %d' % conf.get_int('hello', 'python', -1)) conf.set_int('hello', 'python', 4) log('Testing to get it (after setting it): %d' % conf.get_int('hello', 'python', -1)) log('Saving configuration...') conf.save() 

And the result:

     ... d ......trunkserviceNSClient++.cpp:952 Loading plugin: PythonScript... e nkmodulesPythonScriptPythonScript.cpp:181 Hello World e nkmodulesPythonScriptPythonScript.cpp:181 Got it: alias e nkmodulesPythonScriptPythonScript.cpp:181 Testing to register a function e nkmodulesPythonScriptPythonScript.cpp:181 Testing to register settings keys e nkmodulesPythonScriptPythonScript.cpp:181 Testing to get key (nonexistant): -1 e nkmodulesPythonScriptPythonScript.cpp:181 Testing to get it (after setting it): 4 e nkmodulesPythonScriptPythonScript.cpp:181 Saving configuration... d ......trunkserviceNSClient++.cpp:717 NSClient++ - 0,4,0,77 2011-07-06 Started! l rcenscptrunkservicesimple_client.hpp:26 Enter command to inject or exit to terminate... commands l rcenscptrunkservicesimple_client.hpp:12 Commands: l rcenscptrunkservicesimple_client.hpp:12 | py: This is a sample command py d ......trunkserviceNSClient++.cpp:1096 Injecting: py... e nkmodulesPythonScriptPythonScript.cpp:181 inside proc: py d ......trunkserviceNSClient++.cpp:1126 Result py: OK l rcenscptrunkservicesimple_client.hpp:12 OK: ... 

The resulting settings file looks like this:

     ... ; THis is stuff for python [hello] ; KEY - This is a key python=4 ... 

So it is looking pretty nice I think. Next thing is to create proper
function bindings so you can actually create monitoring scripts using
python. // Michael Medin

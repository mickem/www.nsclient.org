Title: Nightly build with python script module
Author: mickem
Status: published

The first nightly build witch includes the PythonScript module is out.
The module has support for most things but still lacks some of the new
features of 0.4.x such as channels but that will be added in the near
future. I am linking this with python 2.7 which needs to be installed
for it to work but I am unsure which versions of python are supported
but hopefully a few more (but not I guess 3.0 as it is a "new" version).
This is pretty new for me so please let me know anything that does not
work in regards to linking and platforms and such. Also note that the
x64 versions requires x64 version of python. Scripts are loaded in the
following order: 1. absolute path 2. ./scripts/python 3. ./scripts So it
makes sense to put all python script inside the python folder. The
sample script (found inside scripts/python) which looks like this
(subject to change):

     from NSCP import Settings, Functions, Core, log, status core = Core.get() def test(arguments): log('inside test') for a in arguments: log('Got argument: %s'%a) (retcode, msg, perf) = core.simple_query("normal", []) if msg != "ok got: ": return (status.CRITICAL, "Test failed") (retcode, msg, perf) = core.simple_query("normal", ["hello"]) if msg != "ok got: hello": return (status.CRITICAL, "Test failed") (retcode, msg, perf) = core.simple_query("normal", ["hello", "world"]) if perf != "'args'=2": return (status.CRITICAL, "Test failed: -%s-"%perf) return (status.OK, 'Tests ok') def normal(arguments): log('inside normal') for a in arguments: log(' | Got argument: %s'%a) if arguments: return (status.OK, 'ok got: %s'%arguments[0], "args=%d; "%len(arguments)) return (status.OK, 'ok got: ', "args=%d; "%len(arguments)) def no_perf(arguments): log('inside no_perf') for a in arguments: log('Got argument: %s'%a) return (status.WARNING, 'I am ok') def no_msg(arguments): log('inside no_perf') for a in arguments: log('Got argument: %s'%a) return (1) def no_ret(arguments): log('inside no_perf') for a in arguments: log('Got argument: %s'%a) def init(alias): prefix = 'py_' if alias: prefix = '%s_'%alias log('Hello World') conf = Settings.get() val = conf.get_string('/modules', 'PythonScript', 'foo') log('Got it: %s'%val) log('Testing to register a function') fun = Functions.get() fun.register_simple('%stest'%prefix, test, 'This is a sample command') fun.register_simple('%snormal'%prefix, normal, 'This is a sample command') fun.register_simple('%snop'%prefix, no_perf, 'No performance data') fun.register_simple('%snom'%prefix, no_msg, 'No performance data') fun.register_simple('%snor'%prefix, no_ret, 'No performance data') log('Testing to register settings keys') conf.register_path('hello', 'PYTHON SETTINGS', 'This is stuff for python') conf.register_key('hello', 'python', 'int', 'KEY', 'This is a key', '42') log('Testing to get key (nonexistant): %d' % conf.get_int('hello', 'python', -1)) conf.set_int('hello', 'python', 4) log('Testing to get it (after setting it): %d' % conf.get_int('hello', 'python', -1)) log('Saving configuration...') conf.save() def shutdown(): log('Unloading script...') 

Necessary configuration to load the sample script:

     [/modules] ; PythonScript - PythonScript... PythonScript= ; A list of scripts available to run from the PythonScript module. [/settings/python/scripts] py2=test.py 

So as you can see it supports settings (getting/setting/writing) as well
as "running other commands" and exposing commands. The main benefit to
using python scripts over "normal python scripts" are that they better
integrate with other aspects of NSCP. // Michael Medin

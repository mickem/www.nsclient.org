Title: 2006-04-04 New version
Author: mickem
Status: published

I really don't want to release this as I haven't had time to test it
properly (and see what happened last time I didn't test properly). But
hopefully it will at least work better then the previous build.
'''NOTICE''' A major change is that the NSC.ini file now needs an option
to allow NSClient++ to read it (so if that is missing (and it most
likley is as it is a new option) NSClient++ wont even start!
\[Settings\] ; ;\# USE THIS FILE ; Use the INI file as opposed to the
registry if this is 0 and the use\_reg in the registry is set to 1 ; the
registry will be used instead. use\_file=1 If you dont add the above to
your setting file you will endup with the following: e
.NSClient++.cpp(162) Could not find settings: No settings method
specified, cannot start e .NSClient++.cpp(106) Service \*NOT\* started!
The reason for this is that you can now have the settings in the
registry if you so wish. (to test this enable the RemoteConfiguration
module and try the follwoing: NSClient++.exe RemoteConfiguration ini2reg
NSClient++.exe RemoteConfiguration reg2ini This is not perfect (actually
it is sort of buggy so roundtripping is not a good idea, but you can
move from INI -&gt; reg without problems) The RemoteConfiguration has
\*major\* security implication so I wouldn't use it unless you really
want to (you can use it for moving the registry but safely enough
though) but leavnig it there means anyone with NRPE access can
reconfigure you client (not a very secure thing). 2006-04-04 MickeM \*
Fixed a few more bugs to the INI/REG readers \* Could all magicians stop
trying to kill me? \*Please\* i don't like to die! \* Damn necromancers!
stop 0wning my ass all the time! \* Added API for saving/reading
settings \* Added REG/INI parsers \* \*NOTICE\* You need to add an
option (use\_file=1) to your nsc.ini file or new builds wont work. \*
Oblivion f\*cking roxx! \* Fixed bug in INI-file reader (memory leak) \*
Fixed bug in CheckFile (now dates work correctly)

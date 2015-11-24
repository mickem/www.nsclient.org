Title: First RC for the 0.3.6 version!
Author: mickem
Status: published

Nothing major new but have been tested on NT4 and a few other images to
make sure the new building subsystem and such works. Will do some more
load and performance tests and unless there are any bugs new version
will be out in a few days. But please take the time to try it out and
help me find any bugs. I also took the time to rename all files making
it simpler to find them now they are sorted on version instead of on
platform. New features: \* Allows specifying service name with
start/stop/install/uninstall to change the default name of the service.

     2009-01-30 MickeM * Added support for changing name and description of service from the /install command line NSClient++ /install [gui] [start] [service name] [description] NSClient++ /uninstall [gui] [stop] [service name] NSClient++ /start [gui] [service name] NSClient++ /stop [gui] [service name] 

// Michael Medin

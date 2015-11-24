Title: Updates on the 0.4.x branch
Author: mickem
Tags: 0.4.0, status
Status: published

Hello everyone! I have been working quite hard on the 0.4.x branch this
summer (instead of fixing bugs in the 0.3.x branch) and things are
finally starting to look good. Right now the following is implemented:
\* Settings subsystem (old, ini and registry) \* New plugin API (which
is based off google protocol buffers) \* New Settings client (for
plugins, which is wicked cool) \* NRPE client/server (all based off
boost::asio) \* NSCA client \* CheckDisk, CheckEventLog,
CheckExternalScripts, CheckHelpers, CheckSystem have all been ported and
works \* FileLogger have also been ported \* The new scheduler is
working (still needs a better grouping support though) What is currently
missing is: \* LUAScript, CheckTaskSched, CheckWMI \* .net wrapper
plugin \* NSClientListener (check\_nt) \* SysTray (a lot of work is
required here and probably wont make it into 0.4.0) \* The installer
(probably a lot of work to handle upgrades and such) \* Improve the
scheduler to handle groups and such. So we are getting fairly close to a
set of alfa builds (sans installer) and I hope to have most of the above
done in a few weeks. It would be interesting in the next few weeks to
get some people interested in testing it out and helping me with
migration issues and how you like the new stuff. // Michael Medin

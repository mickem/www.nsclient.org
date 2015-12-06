Title: New build 0.5.0 is out!
Authors: Michael Medin
Tags: nightly,nsclient++,0.5.0
Status: published

This is a massive bug fix version and I would almost say that 0.5.0 is starting to come along nicely.
There are a few structural changes I am contemplating but most of the major tings are there.
If you want to take it for a spin you can visit the download page [here](/download/0.5.0/).

The main highlights in 0.5.0 are internals and bugfixes. The most obvious changes are metrics as well as a rewamped much improved web UI.
In this build have a plethora of minor enhancements and bugfixes (over 30 defects have been resolved on github).

Full changelog can be found here:

2015-11-20 Michael Medin

* Fixed #185 extract_perf should now work as expected
* Fixed #154 Added escape-html flag to all check commands and escape html option to all real time filters.
* Added support for -a to check_nrpe command (Fixed #158 )
* Fixed issue when parsing commandline with first otion as short
* Fixed #201 negative perf data in checks
* Renamed status to task_status as it clashes with regular status (Fixed #170)
* Fixed issue with atomic functions missing in older boost
* Added unit test for scheduled tasks
* Added __file__ in python script
* Fixed so uninstalled is called for unit tests
* Fixed #207 Return error when powershell script not found
* Fixed #206 Added support for checking multiple times with check_pdh and rrd buffers
* Fixed a build with older versions of boost issue.
* Fixed #198 CheckLogFile not working if files does not exist on startup

2015-11-19 Michael Medin

* Added metrics submission and fetching to python scripts
* Added ability to run visual processes in the UI session.
  Two new keywords: display controls if the process is showed and session controls which process the session is run in.
* Added support for classifying service and filtering services based on classification

2015-11-18 Michael Medin

* Added test client command metrics to display all metrics
* Fixed option bug in WEBServer command line
* Fixed metrics in WebUI
* Added metrics to internal scheduler
* Fixed missing result in some command line execs
* Fixed services showing twice in service list
* Added showing location using nscp settings --show
* Fixed pressing ctrl+c on command line

2015-11-16 Michael Medin

* Fixed (back) formating in graphite
* Fixed broken metrics ui
* Fixed default values in graphite
* Fixed reload of counters
* Fixed collection stratgey value in web ui
* Fixed default syntax for eventlog as well as a possible API issue?
* Added support for space and strings in column split/line split
* Fixed CheckLogFIle realtime
* Fixed so clients cant override with no target
* Added post option to only post process build on cli
* Fixed support for old pelican
* added --port to nscp nrpe install
* Fixed regression issue in new harmonized scheduler
* Fixed segv in CLI builder

2015-11-15 Michael Medin

* Fixed check_nrpe in installer
* Moved overiden key to the end in the installer
* harmonized schedulers
* Updated some installer files (web/docs)
* Added ugly but working filter list for metrics
* Fixed caching setting random keys in webui
* Added restart to nscp service
* Fixed sample python script cli
* Fixed exec alias in python script cli
* Fixed graphite paths for mestrics
* Added total to check_process

2015-11-14 Michael Medin

* Added build commandline options
* Added build command option to build script (to skip configure)
* Fixed issue with missing command help being target all modules
* Fixed issue with default not beeing set as template
* Fixed issue with python scripts and script arguments
* Fixed some socket bugs in web ui
* Added filtering to query and module
* Added templates to PythonScript
* Fixed metrics (with new py)
* Fixed issue where default was not marked as template
* Tried to improve error handling for ajax requests
* Fixed logout/login issue in webui
* Fixed disk graphs in WebUI
* Added thread count to scheduler metrics
* Added template for schedules
* Fixed some PDH issues and improved error reporting
* Fixed missing default section in settings

2015-11-13 Michael Medin

* Fixed some issues in setting dialog
* Added feedback to loading modules as well as proper save
* WebUI added help to settings dialog (about tabs)
* WEBUI: Changed to save menu is always shown and added auto save support
* Added metrics support to clients and added metrics sending to graphite client

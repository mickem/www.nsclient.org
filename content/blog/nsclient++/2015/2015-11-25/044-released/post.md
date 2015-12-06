Title: NSClient++ 0.4.4 released
Author: mickem
Tags: release,nsclient++,0.4.4

The next, not to major, milestone in NSClient++ history is written today when I change the status of the latest 0.4.4 to stable.
This version is a minor update which brings a new installer as well as some minor enhancements an fixes.
This is in essence a continuation from 0.4.3 and a drop in replacement. The reason we have a new version that the installer has changed so for those who has packaged the installer there might be some tweaks.
Unfortunately this version does not fix the "count" issue many people have been facing but you can always grab 0.5.0 which is pretty stable as well but has more changes and might be a bigger change in terms of monitoring.
This versions apart from a new improved installer also features a fix for a pretty nasty memory leak in check_drivesize.
The are some minor enhancements which have been back ported from 0.5.0 and if you have a feature you wan backported do let me know as a lot of the things from 0.5.0 can easily be backported.

The new installer, as I have stated before, feature a monitoring tool option which can be used to get NSClient++ setup for your favorite monitoring tool (currently only op5). This feature was developed and sponsored by Op5 so a massive thanks to them for that, and to everyone else: pleas help me add more monitoring tolls to the installer!
You can find the new version [here](/download/)

![screen-shot]({static|installer.png} "New installer")

# Using the new installer.

First off you can se the monitoring toll using the MONITORING_TOOL options.
So if you are using op5 you would run:

    msiexec /i <MSI> MONITORING_TOOL=OP5

But as I said you can also use a new keyword to set arbitrary keys on command line.
This is using the new CONF_SET key. This has a rather arcane syntax which is partly inherited from msiexec.
In essence it is a semi colon separated list of path;key;value;path;key;value.

    msiexec /i <MSI> CONF_SET=/modules;CheckSystem;enabled;/modules;NRPEServer;enabled

This would enabled CheckSystem and NRPEServer which can already be done using the existing keys CONF_NRPE as well as CONF_CHECKS.
But while those keys are great for setting Checks and NRPE there has previously not been any way to set arbitrary keys.

The last new option is CONF_INCLUDES where you can specify configuration files to include.
This is used by the installer to setup the include for op5:s config but you can use it as well by setting an include to your own config.
You have to manually place the config file there but that is easily achieved with your package manager or install script.

    msiexec /i <MSI> CONF_INCLUDES=test;test.ini

// Michael Medin

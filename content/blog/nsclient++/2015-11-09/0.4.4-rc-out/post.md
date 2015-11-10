Title: NSClient++ 0.4.4 RC out
Author: mickem
Tags: release,nsclient++,0.4.4
Status: published

Some great news well overdue. 
While I have been working dilligently on both 0.5.0 (which was previously called 0.4.4) I have also been working together with http://op5.se to create a brand new installer for NSClient++. This new instakller is now avalible in 0.4.4 (the reason I bumped versions was since this is potentially a big change if you have customized the installer script). You can find the the download [here](/download/0.4.4/)

The main new obvious thing you will see is this new dialog:

![screen-shot]({static|installer.png} "New installer")

And while this might seem like a collaboration between NSClient++ and op5 it is not instead it is the first step of hopefully many to create support for all monitoring systems out there.
So if you have a great "base configuration" or if you are involved in a monitoring tool do let me know and I will happily add it.

While this is the most obvious change it is probably the least important one (unless you are a op5 user).
The major changes are all under the hood and relate to how the installer work.
It should now work much better and give you greater control as well as added flexibility.

It has long been possible to customize the installer with some random half undocumented keywords.
This has been somewhat error prone and not always working as expected been fixed thanks largely to op5 sponsoring this fix.
But we also have some new options which makes it more flexible as you can set arbitrary keys on command line as well as add included files.

# 0.5.0 progress

In other news we also have builds out for 0.5.0 which has a brand new configuration UI as well as some other cool features and many bug fixes.
I will post some more information about that in the next few days... Currently I am trying to get some thing together for OSMC next week.

# Using the new installer.

First off you can se the monitoring toll using the MONITORING_TOOL options.
So if you are using op5 you would run:

    msiexec /i <MSI> MONITORING_TOOL=OP5

But as I said you can also use a new keyword to sert arbitray keys on command line.
This is using the new CONF_SET key. This has a rather arcane syntax which is partly inherited from msiexec.
In essence it is a semi colon seprated list of path;key;value;path;key;value.

    msiexec /i <MSI> CONF_SET=/modules;CheckSystem;enabled;/modules;NRPEServer;enabled

This would enabled CheckSystem and NRPEServer which can already be done using the existing keys CONF_NRPE as well as CONF_CHECKS.
But while those keys are great for setting Checks and NRPE there has previously not been any way to set arbitrray keys.

The last new option is CONF_INCLUDES where you can specify confioguration files to include. 
This is used by the installer to setup the include for op5:s config but you can use it as well by setting an include to your own config.
You have to manually place the config file there but that is easily achived with your package manager or install script.

    msiexec /i <MSI> CONF_INCLUDES=test;test.ini

// Michael Medin

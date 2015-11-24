Title: Alpha build of 0.4.2
Author: mickem
Tags: 0.4.2, nightly
Status: published

A first alpha build of 0.4.2 is out in the download section.

It is important to understand this is **NOT PRODUCTION READY**. There
are numerous things which is **NOT FINNISHED**.

But I want to get feeback on the new filters and check commands so
please feel free to take it for a spin in a lab enviornment. The best
way to get start is install nsclient++ and use your existing
configration.

Documentatiojn can be found here: <http://docs.nsclient.org>

Then start nsclient++ in "test mode" where you vcan get help and
information.

Some commands to get you started:

-   check\_cpu\
     Check CPU load
-   check\_cpu help\
     Get help on avalible options for check\_cpu
-   commands\
     List all avalible commands

Please also review my post previously on this blog where I showcased how
to use the new commands. Things NOT included in this build are:

-   Various modules:
    -   CheckWMI
    -   CheckFiles
    -   CheckTaskSched (CheckTaskSched2 is included though)
-   Compatiblity layer:\
     The real version will feature a compatiblity layer which will
    convert MaxWarn=4 into "warn=count &gt; 4".\
     This has yet to be added. THis means NONE of your existing checks
    currently works. But as I said this will be fixed in comingbuilds.
-   check\_nt support:\
     check\_nt has previously been relying on hardcoded special commands
    which will no longer be replaced instead it will be utilizing the
    regular commands. THis is not yet implemented to all chekc\_nt
    commands will cause errors.
-   Quality check: THis is a development version so I have yet to test
    this extensivly.
-   NT4 support (perhaps even windows


Title: 0.4.2 build 20 (verified in xp->2008)
Author: mickem
Tags: 0.4.2, nightly
Status: published

The last build of 0.4.2 have now been verified from Windows xp to
Windows 2008R2 (will do 2012 over the Weekend). The commands which
should work:

**CheckSystem:**

-   check\_cpu\

    <http://docs.nsclient.org/reference/CheckSystem.html#CheckSystem.check-cpu>
-   <span style="line-height: 1.5em;">check\_uptime\
    </span><http://docs.nsclient.org/reference/CheckSystem.html#CheckSystem.check-uptime>
-   check\_service\

    <http://docs.nsclient.org/reference/CheckSystem.html#CheckSystem.check-service>
-   check\_process\

    <http://docs.nsclient.org/reference/CheckSystem.html#CheckSystem.check-process>
-   check\_pdh\

    <http://docs.nsclient.org/reference/CheckSystem.html#CheckSystem.check-pdh>
-   check\_memory\

    <http://docs.nsclient.org/reference/CheckSystem.html#CheckSystem.check-memory>

**CheckTaskSched:**

Please note that the "old" CheckTashShed1 and CheckTaskSched2 have been
merged into a single module which will use correct mechanism
automatically.

-   check\_tasksched\

    <http://docs.nsclient.org/reference/CheckTaskSched.html#CheckTaskSched.check_tasksched>

**CheckDisk:**

-   check\_drivesize\

    <http://docs.nsclient.org/reference/CheckDisk.html#CheckDisk.check_drivesize>

**CheckEventLog:**

-   check\_eventlog\

    <http://docs.nsclient.org/reference/CheckEventLog.html#CheckEventLog.check_eventlog>

**CheckLogFile:**

-   check\_logfile\

    <http://docs.nsclient.org/reference/CheckLogFile.html#CheckLogFile.check_logfile>

// Michael Medin

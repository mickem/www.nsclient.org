Title: NSClient++ 0.4.3.143 has been released and trac is dead...
Author: mickem
Tags: 0.4.3, release
Status: published

Hello trac legacy users and merry Walpurgisnacht (a few days late)...

As some may have noticed I have finally killed the "old" trac site once
and for all, I have hopefully redirected traffic to the correct place,
if not please do let me know.

Now on to more important stuff.

NSClient++ 0.4.3.143 has been released
--------------------------------------

This is mainly a bugfix release which has some minor new features (in
the form of a check\_ping command). [Head over to the download section
to get the goodies](http://www.nsclient.org/download/).

For details feel free to peruse the changelog after the
break:<!--more-->

**2015-04-29 Michael Medin**

-   Improved handling around connection failures
-   \#142 Improved security when external scripts fails command lines
    which may contain password are no longer returned

**2015-04-27 Michael Medin**

-   Improved the logging around connection failures
-   Improved the reporter syntax: reporter.exe send
    b1438ab2-20a3-4b2d-bc30-7c3033c084e1.dmp

**2015-04-08 Michael Medin**

-   \#139 Added support for showing file dates in local time (not
    just UTC)
-   Added check\_ping command and CheckNet module
-   Fixed a few potential crashes with check\_nt

**2015-03-24 Michael Medin**

-   \#123 fixed CheckAllOthers
-   \#124 Fixed problem count variable
-   \#131 Added support for service= to check\_service
-   A lot of infrastrucutre changes and build fixes

**2015-02-23 Michael Medin**

-   Fixed check\_files empty message to say files not drives.
-   \#114 Fixed issue with empty-state which was ignored
-   A lot of infrastrucutre changes and build fixes

**2015-02-14 Michael Medin**

-   Fix incorrect variable in check\_page\_filter()
-   Add pct to check\_pagefile This is basically a clone of f90ab0b
    which added pct to check\_memory.

 

Title: New release candidate for 0.4.4 is out!
Authors: Michael Medin
Tags: rc,nsclient++,0.4.4
Status: published

The main highlights here is a fix for incremental updates (i.e. updating from 0.4.4.x to 0.4.4.y) as well as a fix for a memory leak in check_drivesize. As always head over to the download page to get it [here](/download/0.4.4/).

For those new to 0.4.4 is is a continuation of the 0.4.3 branch but with a new updated installer. The installer adds some new features which makes it simpler to install it automatically. There are also a bunch of bug fixes and minor feature enhancements brought in from 0.5.0.

![screen-shot]({static|installer.png} "New installer")

If there are no new more issues this will be the official stable release in a few days or so so please help out with testing, especially the people who has seen the memory leak!

The full changelog can be found here:

* Added post option to do only post install action on build
* Fixed installer upgrade issue when upgrading from build revisions #164
* Fixed #206 Added support for checking multiple times with check_pdh and rrd buffers
* Fixed drive letters with single character
* Fixed certificate creation in webserver (and removed dependency on applink)
* Fixed building on visual studio 2015
* Added showing location using nscp settings --show
* Fixed services showing twice in service list
* Added noop as channel target to discard message
* Fixed memory and resource leaks #199

Title: Linux love: RPM packages for centos 7.0
Author: mickem
Tags: 0.4.3, linux, nsclient, release-candidate
Status: published

Yaaay!

After weeks and weeks and possibly weeks.

The [very first Linux
packages](http://www.nsclient.org/files/beta/NSCP-0.4.3.60-x86_64.rpm)
are available. Consider this very very experimental.

To install it you grab the package and do the regular:

    sudo yum install nscp-4.3.60-x86_64.rpm

After this (since it is systemd) you can reload and start it like so:\
 sudo systemctl start nscp.service

To make it slightly more useful you can do:

    sudo nscp nrpe install
    sudo systemctl restart nscp.service

Which will setup the NRPE agent is "safe" mode which means encrypted
nrpe using certificate, you can also set it up in "secure mode" which
would be trusted certificates but this is another blog post.

Finally to make ting slightly more easy you can do:

    sudo nscp web install
    sudo nscp web password --password
    sudo systemctl restart nscp.service

To activate the built in web server, next point your web browser to
http://localhost:8443

Everything works pretty much the same, meaning you can use all your
existing plugins as well as all your regular NSClient++ commands and
features. Not all checks are native on Linux yet (it is a work in
progress to migrate everything but in the mean time all normal plugins
work as they use to do).\
 Please note that the massive size is due to Linux being statically
linked (see other post about windows going dynamic). I will try to fix
this in the near future but I wanted to get some feedback on the whol
package thingy and all that and more importantly get some bug reports!

In addition to nscp you also have check\_nrpe which supports
certificates making it a tad more secure the regular stuff. once I have
some time I will split the packages off into subpackages to make it
simpler to install "just the nrpe client" and not the entire NSClient++
server.

 

Just a few words on the Linux layout:

-   /etc/nsclient/nsclient.ini
-   Configuration
-   /usr/sbin/nscp\
     Main server daemon
-   /usr/bin/check\_nrpe\
     Check\_nrpe client
-   /usr/share/nsclient\
     Web folder, certificates and what not
-   /usr/lib/nsclient\
     Modules
-   /var/log/nsclient/nsclient.log

Everything is owned by the nsclient user which also runs the daemon. The
reason I mention this is partly to make exploring NSClient++ on linux
simpler but also to get some feedback on whether this is good or bad...

**Now please please, all the Linux people out there, hit me with
comments feedback, ideas thoughts, flame, pull requests what not...**

EDIT: Download link removed since 0.4.3 has been released, please grab
that instead.

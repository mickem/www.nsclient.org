Title: 0.4.3 beta 1 (build 40)
Author: mickem
Tags: 0.4.3, beta, updates
Status: published

Greeting CloudFlare proxy!

Finally after weeks of dreadful boring but time consuming build issues
0.4.3 beta 1 is here!

0.4.3 will probably be the biggest update from a usability improvement
perspective ever (but I always say that). The idea was that 0.4.3 would
be a minor update, and in many ways it is, but I just can't shake the
feeling that the WEB-UI is a game changer.

<!--more-->

So what is new you ask?

**Web UI**

Well the WEB UI is brand new and a nice way to configure NSClient++ both
if you are an advanced user or if you are a new user. The WEB UI will in
the future be extended to accepting and submitting metrics and checks as
well as remotely connect to a running NSClient++ instance. But currently
if you have the WEBUI module (WEBServer) you can load/unload modules
configure modules execute queries as well as run various commands. I
would say that this can effectively replace the "nscp test" mode.

![webui](/images/blog/webui-300x297.png)

**New improved "test mode"**

Since I reworked the WEB test client I did the same for the regular test
client os it now has many new commands to load and unload modules as
well as previously execute commands. You help for details.

**NRPE enhancements**

I have spent a lot of time enhancing the NRPE experience for instance
the multi package patch is enabled by default. Adding security and
certificates is now much easier. And there is a command line client for
configuring NRPE. the WEB-ui has the same thing and this will be coming
to many more places so keep looking out for it.

>     nscp nrpe install
>     Enabling NRPE via SSH from: 127.0.0.1
>     NRPE is currently reasonably secure using ${certificate-path}/certificate.pem and ${certificate-path}/certificate_key.pem.
>     Arguments are NOT allowed.

**Breaking change: no out-of-the box support for NRPE legacy**

If you are using NRPE you are in for a chock!

In 0.4.3 **we will no longer support** the rather insecure regular NRPE!
You can still **enable support** but you have to do so (in the installer
or using the command line mode). So keep a heads up when you run the
installer so you wont miss it.

The idea is that when NSClient++ ships a new check\_nrpe will be
provided which wont have the limitations of the old one.

**Dotnet love!**

Dot net has received some well deserved love and now actually works,
there is even built-in protobuf support which means you no longer need
to hand craft messages or use JSON. We also proved and build a sample
plugin so you can see how to do it.

**JSON!**

All protobuf messages now map directly to corresponding protobuf
messages which means you can now if you like use JSON for everything
instead of protobuf if you are writing scripts.

**Bug fixes**

The focus has (and still is) on bug fixes so NSClient++ contains
numerous bug fixes and enhancements in addition to the above mentioned
changes. As I have said before the idea with 0.4.3 is to make a bugfixed
0.4.2 so there wont be that many changes.

**Whats missing?**

This is an early beta version and there a lot of things missing. Most
important is that I will go through all defects both on github and trac
and try to close as many as possible. But we are also missing some core
features.

-   WEBClient\
     The WEBClient will be used to run check\_nrpe like commands over
    the WEB-port as well as talk to external systems
-   Linux love\
     I still need to fix the Linux build so it works as well as create
    Linux packages
-   WEB-UI: Query tab\
     The query tab which was the first I did needs some more love.
-   Documentation\
     I need to update the documentation in some regards but more
    importantly make sure I can have multiple versions on docs which it
    currently does not support so docs is 0.4.2 as of yet (you have to
    use the supplied PDF currently for 0.4.3 or the command line help).

**Just let me re-iterate once more: legacy check\_nrpe requires
configuration!**

Full changelog: <https://github.com/mickem/nscp/blob/master/changelog>

[You can download it from the beta section in
downloads.](http://www.nsclient.org/download/beta/ "Beta versions")

 

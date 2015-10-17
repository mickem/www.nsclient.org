Title: Web and REST updates
Author: mickem
Tags: 0.4.3, nightly, status, web
Status: published

Greetings baidu search bot!

As always, sorry for being very very unactive last few months but work
has been busy busy busy.\
 Anyways I have started to work on the new UI for NSClient++ as well as
the REST support. This comes in the form of the WEBServer module which
is now in the trunk on github.

The idea is that this module shall provide two things:

1.  A configuration/administration UI
2.  REST support

This is a bit of a combination as the admin UI will be written as a web
app using the REST API. Currently I have written a prototype just to
play around a bit and see what we can expect and thus far I am very
satisfied:

The first screen shows a list of all available commands (queries) and
allows me to execute them.

![](/images/blog/nsclient-webserver-screenshot-001_f_improf_629x548.png)

Clicking on execute will execute the query and display the result:

![](/images/blog/nsclient-webserver-screenshot-002_f_improf_612x365.png)

As you can see this is implemented using bootstrap which means we have a
nice and modern look-n-feel and since it is all using the REST API all
this can be done using your favorite front end/client as well. Now this
is a prototype currently so there is no security etc etc so this is
nothing I would recommend anyone to activate especially not in
production. But if you want to try it out you can grab the source code
and build it and then activate it like this:

    [/modules]
    WEBServer = enabled

Then you start NSCLient++ in test mode and browse to
http://localhost:8080. This will be available in nightly builds in a few
days as well and hopefully sometime in the new few weeks it will get
some login and basic security and then you can start using it.

The main planned features are:

 

-   Show modules and load/unload them
-   Configure NSClient++
-   Enable/disable debug log
-   See the console log (no more need to use "nscp test")
-   Access documentation (no more need for the PDF)
-   Execute commands and queries

Please do let me know if there is anything else you think we should add!

Title: New build: working web-ui
Author: mickem
Tags: 0.4.3, demo, nightly, ui, web
Status: published

**Hello duck-duck-go bot**(though they probably don't have their own bot
I guess...)

A new build is out (soon, had to fix a js error on the log page) which
showcases a workable prototype for the WEB UI. I think the WEB UI is
pretty cool and would really love feed back on it.

It is a prototype and as such please don't use this in production!

So what can you expect?

Settings
--------

Browsing the settings works (there is an error generated every time you
enter the page though but that is harmless).

![](/images/blog/web_ui_001_f_improf_591x546.png)

Clicking a "section" (path) you can browse the keys and see the
description as well as edit it. Once you have saved your settings a
popup is showed which asks if you want to persist changes to disk.

![](/images/blog/web_ui_002_f_improf_817x648.png)

You also have the option to create new "unknown keys" by clicking add,
or you can use this as a shorthand add option.

![](/images/blog/web_ui_004_f_improf_325x330.png)

Restart and Mobile
------------------

If you save changes to disk you can select restart NSClient++ to
activate the changes. In the future you will be able to save settings to
a custom store so you can create a new config and/or create configs for
your clients.

![](/images/blog/web_ui_005_f_improf_328x156.png)

![](/images/blog/web_ui_006_f_improf_680x187.png)

The UI is designed on bootstrap so it is mobile aware and everything
works handsomely on a mobile device with the infamous hamburger menu.

![](/images/blog/web_ui_003_f_improf_382x487.png)

Running things
--------------

Apart from settings you can also as I showed before list and execute
commands

![](/images/blog/web_ui_007_f_improf_765x325.png)

View log in almost realtime
---------------------------

Lastly which I think is really cool there is a built-in log viewer so
"nscp test" will soon have a fully fledged modern web cousin.

![](/images/blog/web_ui_008_f_improf_497x439.png)

Please download the new build (0.4.3.9)
from <https://nsclient.org/nscp/downloads> and let me know what you
think!

Apart from the WEB UI work I have spent some time over the weekend
answering almost all questions on the community site for the past few
weeks, as I have said before I have been mad busy at work which is now
starting to slow down so I will be picking up the NSClient++ pace
again...

 

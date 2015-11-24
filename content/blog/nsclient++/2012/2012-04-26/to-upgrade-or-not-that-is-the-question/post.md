Title: To upgrade or not that is the question?
Author: mickem
Tags: 0.4.0
Status: published

Well, NSClient++ 0.4.0 will be released in a few days so I guess the big
question everyone has right now is to upgrade or not. And it is a big
question which I have been pondering for quite some time. I usually
pride myself in the quality of NSClient++ and it is not that "it is bug
free" but it has had few critical bugs over the years (since 0.3.0) but
with 0.4.0 it is to large degrees a rewrite which means it has thousands
of new lines of code as well as thousands of changed lines of code. This
of course all adds up thousands of new bugs. To try to combat this I
have introduced unit tests as well as been running betas and release
candidates for quite some time. Yet I cant help but feel a bit scared
about releasing this: will this be big heap of bugs or not? My
recommendation for upgrading to 0.4.0 is colored by this and caution is
what I advocate. I think you can classify people into three groups. 1.
'''I need/want/covet new cool stuff.''' In this case you have no option
but to upgrade. But remember do so with care and read the "upgrade for
advanced user" section below. 2. '''I don't need new features but I
don't mind experimenting a bit.''' Definitely a candidate for upgrading
but read the "upgrade for existing user" section below. 3. '''I have
5000 production critical servers and my boss gets really really mad.'''
You should start (in your lab) to upgrade and report any issues so you
can feel secure and upgrade all your machines once 0.4.1 is here! You
should read both sections below. == Upgrade for existing users. == The
current recommendation is to upgrade the client but not the
configuration. The main reason for this is that the old configuration
"should work" in 90% of all cases. And since configuration migration can
have some issues migrating now means you are certain to be affected by
any bugs where as if you migrate later on you can most likely avoid any
issues. == Upgrade for advanced users. == This is not so difficult as it
may sound you simply run the following command to migrate your old
configuration to the new configuration. But it is important tha you
validate your configuration to make sure everything works as it should.

     nscp settings --migrate-to ini 

Also note that there are a number of new features you can use in the
configuration so be sure to try out the "generate full config" command
below.

     nscp settings --generate settings --add-defaults 

There is also a number of new modules and if you want to see what they
provide in the form of configuration you can run the following command:

     nscp settings --generate settings --add-defaults --load-all 

The last two commands will create a lot of noise so it is recommended
(until the arrival of the --remove-defaults) to note base your new
configuration from them but use them as inspiration. == Conclusion ==
Hopefully that's answers all questions if not feel free to ask. Thus the
general guidelines are: 1. Don't upgrade configuration unless you
want/need new features and/or want to spend some time tweaking your
configuration. 2. If you migrate your configuration make sure you
validate it (and please report anything which doesn't work out of the
box)! 3, If you generate default configuration make sure you remove what
you don't need (defaults are good). 4, Make sure you run this in you lab
before you push it onto all your servers. // Michael Medin

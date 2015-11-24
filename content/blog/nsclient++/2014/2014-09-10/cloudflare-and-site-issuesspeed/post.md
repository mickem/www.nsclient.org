Title: CloudFlare and site issues/speed
Author: mickem
Tags: 0.4.3, nightly, website
Status: published

**Nín hǎo Sogou web spider 4.0**\
 Ní hào mǎ\
 (which is Chinese for hello how are you ish)

Just thought I'd let you know I have enabled
C[loudFlare](https://www.cloudflare.com/) caching in front of
nsclient.org so hopefully downloads and web site will be a tad faster
but on the other hand javascripts and css and what not might be broken.
My cloudflare skills are not what they could be.

So please do let me know if you run into any issues. I am new to the web
optimization game but the site gets a wee bit of traffic and things are
slow on and off so I thought I would try to do something about it.

<!--more-->

The reason behind it is that the site has been terribly slow and has had
a lot of issues lately. So we shall see if this improves things or note.

Interestingly one unexpected benefit of CloudFlare was the statistics
dashboard. The site seems to generate a bit of traffic (and we are only
partially on CloudFlare since DNS changes takes a long time to sync):

 

![Stats from Cloudflare](/images/blog/partially-on-cludflare.png)

If I read this correctly it seems we have several gigabytes per hour
which will hopefully decrease a bit with 0.4.3 since the size has
shrunk.

But this leads me to believe that there probably are several hundred
downloads per day which (if true) would be pretty cool.

On another note...

I did promise some cool updates but since getting 0.4.3 to build
automagically has been a pain things have been a bit delayed. But now we
are back on track and last build seems pretty good. I am currently
fixing some issues in 0.4.2 and will rebuild that as well but hopefully
for the weekend 0.4.3 beta 1 will be out...

 

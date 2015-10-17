Title: Merge..
Author: mickem
Status: published

For those who keep track I have just merged the trunk with the 0.3.6
changes so soon there might be nightly builds from that branch but we
shall see. I have some ideas on re shuffling the order of the "new
features" as well, mainly moving the graphic configuration UI to a later
build (possibly 0.5.x or beyond) and instead focus on moving the sockets
over to boost Asio (a socket library) as well as some other minor
changes. The main reason being that it might allow me to start sketching
on a new "protocol" to "replace" NRPE but we shall see. I am also
working on some improvements to the install (the 0.3.x branch) so there
might be a 0.3.6 version in the near future (a few weeks) which will
have a slightly improved installer. There is also plans on a new
"CheckFile" command with a syntax similar to the EventLog to make it
more useful (it is already there in a sort of beta for 0.3.5). I also
need to go and update the documentation since there is a new version but
that is boring so we shall see when I get around to doing that ;) //
Michael Medin

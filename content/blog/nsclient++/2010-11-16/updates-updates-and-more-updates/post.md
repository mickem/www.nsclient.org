Title: Updates, updates and more updates
Author: mickem
Status: published

Hello everyone. First off: sorry for the lack of updates. My current
project (at work) is often labeled as "the most difficult project in
Sweden". This is of course good. It is a pretty fun project whit a lot
of interesting things going on. We are also very free to choose
implementations and design considerations again amazingly cool apart
from the brilliant guys who voted git in). But there is a huge downside
and that is I currently am working somewhere between 50-60 hours per
week. This means there has been very little time for NSClient++ last few
months. I literally had to work day and night to finish off
presentations for OSMC and hoped that would be the end of it but alas it
was just the beginning and since it has gone from bad to worse. I have
though promised myself I shall try to stop working so much overtime
especially since I don't actually get payed for it :P But I have been
saying that for weeks so we shall see. Anyways, I have today managed to
spend all evening working on a new feature in the trac forum so I can
more easily track which posts have been answered and not. And I plan to
start working through the backlog of questions but it will most likely
take a few weeks so please bare with me in the mean time. I will also do
it in the order "simple to hard" so the harder (and perhaps more
important questions) will have to wait. My intention with the new
feature is to slowly answer ALL questions regardless of when asked so
but old questions will be scheduled for much later. In the mean time I
can give some quick updates there is a few new nightly build of the
0.3.x branch with some minor changes

     2010-11-14 MickeM * Added the "extended NRPE payload packet patch" Should have done this years ago but alas I have not. This allows you to (with a patched NRPE) send and recieve more then 1024 chars (in a backwards compatible way) cf: https://dev.icinga.org/attachments/113/nrpe_multiline.patch To enable this you set the following. The value is the number of packets we allow. [NRPE] packet_count=10 NOTICE for this to make sence you need to extend the "main payload buffer" which will most likely run out. [Settings] string_length=16000 This value "should" be NRPE:packet_count*NRPE:string_length(1024) 2010-10-17 MickeM * Added new command timeout which runs a command in a thread and timeouts after a given time. *NOTICE* this is not a good command to use since it will leak memory/resources when it "kills threads" * Added new command: negate which can alter the result of other commands 2010-09-29 MickeM * Reverted a merge miss in CheckDisk * Added so IN (...) accepts strings without qoutes in the SQL Query syntax of CheckEventlog * Added new "parsing structure" str(...) to create strings in the SQL query without using ticks (') to allow "nasty meta char thingy") * Extended error parsing (eventlog messages) to allow up to 24 arguments (up from 11) 

And the new 0.4.x branch is slowly getting finished. Last few things I
have done is created a better logger (which runs in the background) and
implemented all settings using the new simpler helper framework. After I
finish that I need to diff all plugins to make sure all existing changes
are synced and then we are pretty much ready to go. // Michael Medin

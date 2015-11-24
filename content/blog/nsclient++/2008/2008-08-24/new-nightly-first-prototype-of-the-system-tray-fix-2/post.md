Title: New nightly first prototype of the System Tray fix!
Author: mickem
Status: published

Hello everyone. Finally managed to shake my illness (glandular fever) so
here it is, the biggest one in a while... A new nightly, is up. But
beware this one is a monster (several hundred new lines of code) so take
care when you play around with it. (it '''should be safe''' to run with
the shared session off). To see everything in action do the following:
1. install (unzip or installer) 2. install service (nsclient++ /install)
3. '''DONT''' enable the Systray module. 4. Enable the shared session
(\[settings\] / shared\_session=1) 5. Start (net start nsclient++) 6.
'''WTH'''?!?!?! where did that systray come from you ask? 7. Use the
systry and; - see the logs - see the logs when you '''restart''' the
'''service''' - see the logs '''when''' the '''service crashes''' - stop
('''and start''') the service. In short this is the proper way to make
system trays in "modern" windows. - The service creates (when a user
logs in) a process in the user realm that runs the system tray - The
service and the system tray uses an IPC framework to speak to each
other. Simple, beautiful and elegant...and ohh so dangerous! - First off
I have been ill last few weeks so much of this code has been written
with me having a temperature around 40 centigrades (104 for you over in
the old world) eating only fluid "food" which means quality is not 100%.
- Secondly IPC frameworks are hard to write there are a lot of
considerations and a lot of things that can go wrong. - Thirdly there is
fundamental security issue here, since the "service" (privileged user)
creates and takes instructions from a user (level process) so what
should we allow the user to do? - Forth it is several hundred new lines
of code and a lot of changes. So let me know what you think and in which
direction you want me to take this. This is a prototype in its current
form, but as I said before if you disable the shared session it should
be safe to use the new client (if not let me know) so don't be to
scared. There is a a ton more things I should say here but I think we
should maybe move this to a discussion? // Michael Medin

Title: RC8 out!
Author: mickem
Tags: release-candidate
Status: published

Hello everyone (and yes that is probably only me, since no one ever
comments on theses :) Anyways, new RC out as promised, nothing really
new from last nights build but I have been running some tests and such
to see if I can track down the errant memory leak I found... and I
did... ut I have yet to fix it, but dont worry the leak was in the
shared session code so just disable shared session and you are fine. I
shall (post 0.3.x) I think fix the shared session but depending on how
easy it it this might be fixed before. The highlight from this new RC is
instead the brand new installer! It is much improved and works as an
installer \*should\* so all you "MSI package people" let me know what
you want configurable. The new installer will (after you pick target
directory) read the old config and populate up the parameters used on
the "configure dialog" the dialog "wont save" anything as of yet this
will come in the next version but I wanted to get some feedback on the
contents of the dialog. So if you have any ideas on what you want let me
know!!! (yes... I mean that... let me know!!!) :) Full changelog since
last RC are here:

     2009-03-15 MickeM * New service name (displayname) * New service description 2009-03-14 MickeM * Rebuilt installer UI (still missing write config function) * Added debug entry to log filename used by debug log metrics. * Fixed so alias will not require the allow_nasty_meta_chars option set under external sripts module. 2009-03-02 MickeM * Added catch handlers and error logging to NSCA Thread * Fixed issue with CheckProcState and administrator login! + Added debug module to installer + Added option max-dir-depth to CheckFile and CheckFile2 like so: CheckFile "file=c:test*.txt" filter-size=<24g "syntax=%filename%: %size%" MaxCrit=1 max-dir-depth=0 Will only find files on the "first level" where as max-dir-depth=1 would find all parents and children etc. (-1 is the default and means find all) * Fixed issue with finding sub-folders and *.txt now it will always look for subfolders if they are present 

// Michael Medin

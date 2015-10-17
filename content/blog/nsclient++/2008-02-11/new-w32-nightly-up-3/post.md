Title: New w32 nightly up!
Author: mickem
Status: published

Finally the long awaited (not really, but was a b\*tch to fix)
encryption support for NSCA module has been fixed. We only support:
None, Simple XOR, DES, 3DES (Triple DES), CAST-128, xTEA, BLOWFISH,
TWOFISH, RC2, RIJNDAEL-128 (AES), SERPENT) as they were reasonably
"straight forward" the others had various "problems" and since I dont
really think anyone ever use them I decided to not spend the time to fix
it (let me know if you actually use any of the missing ones and I will
see if I can get it added). The important thing is that you can encrypt
the data if you ask me :). There is also a new module
(CheckExternalScripts) which is similar to NRPE (I would recommend it
over NRPE) in that it can run external scriupts/programs but it has been
streamlined a bit and most importantly if you don't want to use NRPE
(think NSCA) you can still run external scripts and such. And finally I
have improved exception handling quite a bit and hopefully things will
be "more stable". We are starting to com up on the 3.1 release so now
would be a good time to report all bugs and problems... Changelog:

     2008-02-11 MickeM + Added encryption support for NSCA module (about half of the algorithms are avalible, if someone wants to use one not available let me know, and I will try to add it) 2008-02-09 MickeM + New module CheckExternalScripts to handle 1, external script (similar to the old NRPE but in its own module) - Can Check batch/vbs/programs/* - Works with NSCA module (if you don't want to have NRPE at the same time) - Simpler syntax (discarded old and added new section for alias) - Started to add "sample alias" to ease initial setup and give some nice ideas (please provide me with feedback on them) 2008-02-08 MickeM + Added some more default catch handlers (on the "core" side of plugin-calls). 2008-02-07 MickeM + Added default catch handlers to all wrapped plugin calls. 2008-02-05 MickeM * Fixed issue with checkEventLog (sometimes you got the wrong message back) 2008-02-04 MickeM *** Happy Birthday bogi!! :) * Fixed issues with performance counter rendering (mainly checkDisk) 

// MickeM

Title: New built-in crash detection with dump submission using Google breakpad!
Author: mickem
Status: published

Hello everyone, I just released a new version which features Google
breakpad support. This is an initial version so don't use this in
production! In essence what this means is that whenever NSClient++
crashes it will do two things. 1. Send a crash dump to
crash.nsclient.org 2. Restart the nsclient++ service. This is as I said
before an initial version so there is a lot of things you cant really
use yet. The idea is to have tree modes of operation. 1. Automatic:
meaning crashes will be submitted and service restarted 2. Manual: Dumps
will be collected and service restarted. Having a check inside
nsclient++ where you can check for dumps and submit them. 3. Off: Dumps
will be collected. The concept is based around google breakpad which is
(amongst others) what Mozilla uses for Firefox and Thunderbird and
Google uses for Chrome. You can try this out in /test mode using the not
so friendly "assert" keyword:

     nsclient++ /test ... ... assert 

// MickeM

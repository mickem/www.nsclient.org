Title: NSCA Module
Author: mickem
Status: published

First version of the NSCA module is out. Module can be used to supply
passive check results to nagios (instead of active checking). This is a
simple mock-up which lacks many features (encryption to name one) but it
would be interesting to know what people thinks of the "concept" and
also if it "works" in real-world environments. To try the new module: \*
enable the NSCAAgent.dll \* edit \[NSCA Agent\] section \* add your
favorit checks to \[NSCA Commands\] Changlog for the new nightly:

     2007-12-09 MickeM + Added a check if the service is started when running with /test so you get a warning + Improved the socket thread with: * a default-catch * If the socket failes to start we still wait for it to shut down (no error message) + Added first version of the NSCA agent (NSCAgent.dll) (no encryption support as of yet, but will come) 

// MickeM

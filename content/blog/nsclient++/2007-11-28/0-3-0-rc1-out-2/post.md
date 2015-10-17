Title: 0.3.0 RC1 out!
Author: mickem
Status: published

Finally, first release candidate for the 0.3.0 version is out. Let me
know any issues you have and I shall fix them ASAP. A bunch of
minor/major issues have been fixed (mainly some NT4 and UNICODE issues)
in this version and all but 1 ticket for the 0.3.0 series is closed so
hopefully things are looking good. We also have all platforms built ie.
w32/x64/IA64 so feel free to try it on various platforms and OS
combinations. The RC:s are under the x-0.3.0 folder (not nightly) so
make sure you grab the "correct" one.

     2007-11-28 MickeM * Fixed some UNICODE issues with process-listings + Added an error message if the "detected" process enumeration method is not available. + Fixed some more unicode issues Password encrypt/decrypt: #107 * Fixed unicode issues with "external programs" #109 * Fixed so default string for check_nt:s FILEAGE command is "delta" is 5 minutes ago (and not absolute ie. 1970...), Issue #39 + added support for  to check_nt:s FILEAGE command, Issue #39 append: . if you want to use a "custom date" like so: ... -v FILEAGE -l c:windows,Date: %Y-%m-%d %H:%M:%S" -w 5 -c 6 ... Only the above listed % works, and default to 0 so might not be to pretty but works... 

// MickeM

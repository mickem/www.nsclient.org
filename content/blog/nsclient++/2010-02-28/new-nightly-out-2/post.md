Title: New nightly out...
Author: mickem
Tags: disk, nightly
Status: published

A new nightly out. Nothing major just a few fixes to the CheckFile
related module.

     2009-02-26 MickeM * Changed fo missing files and such generate an error * Added option to return error messages to the client [CheckDisk] show_errors=1 (defauilt is off 0) * Added warning message ewhen numerical filters evaluate to zero (and are not 0) * Fixed major issue with date mathing in CheckFile* which was not working at all. 

Note though that this new release is built with a new "kit" ie. new
version of boost, openssl, and what not so things might be a bit more
experimental then usual... // Michael Medin

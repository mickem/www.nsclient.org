Title: Another attempt at a "final 0.4.0 RC"
Author: mickem
Tags: 0.4.0, release-candidate
Status: published

''Build 153''' Almost starting to feel a bit pathetic but hopefully this
means it will be a smoother release. So again '''please, please,
please''' test! Anyways, The main fix is the does-not-start-on-boot
which was due to a problem with the boost library I used to to
thread/process communication (it apparently required DNS to load which
caused timeouts as well as failing the service). Other fixes and
enhancements include NSCA settings parsing/upgrading as well as reworked
the generation command making it possible to generate a settings file
with less "crap" and more things you actually need. I will BTW also in
the next few days write a blog post about using the settings subsystem
from a 0.3.x perspective... '''UPDATE''' This means the FileLgging
module is no longer used/required so please remove that from your config
file (log-to-file is no included in the main program). Full changelog
here:

     2012-04-01 MickeM * Fixed issue with default port for NSCA/NRPE/* clients 2012-03-31 MickeM * Rewritten log implementation from ground up without using crappy boost library which requires DNS :( 2012-03-27 MickeM * Removed some annoying "error" messages * Tweaked FGileLogger a bit to be more "modern" * Changed so file-name expansion is more efficient * Changed so modules are defaulted to 0 in config. * Log levels are case sensetive * Fixed so log level is not read from ini file * improved plugin processing from ini files 2012-03-26 MickeM * Fixed perfoamcen data parsing issue * Fixed external scripts perfoamcen data issue * Fixed boolen flag handling in settings (default generated as false regardless of actual state) * Fixed so "advanced properties" are not generated with --update-defalts * Added some "advanced properties" here and there * Fixed path handling for object 2012-03-25 MickeM * Added last few features to the GraphitePlugin (which is now usable) * Tweaked nscp settings command line syntax a bit to be more flexible and usable... 

// Michael Medin

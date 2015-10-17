Title: New w32 build
Author: mickem
Status: published

This one should work on nt4 so everyone still using that platform feel
free to try it. There is also some other neat features into it mainly
related to the "Configuration" handling

     * Fixed a minor issue in reading registry keys + Added -noboot option to startup used for running command line utilities without booting the client "nsclient++ -noboot RemoteConfigruation ini2reg" for instance + Added fallback to try  and .dll if the module was not loaded (when running command lines) * Migrated 2008 project files to new name and back-ported to 2005 project files. 

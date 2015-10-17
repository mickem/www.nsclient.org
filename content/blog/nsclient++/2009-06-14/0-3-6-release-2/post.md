Title: 0.3.6 Release!
Author: mickem
Tags: 0.3.6, nsclient, release, version
Status: published

Finally after and long overdue is the new version here. This is a major
update and a recommended one as there are memory leaks in the previous
version. The highlight in addition to all the fixes and minor things are
the experimental new installer which allows you to configure some
options while installing NSClient++. The installer should I hope work
better and provide easier error handling and such. The only issue thus
far are some reports on windows 2007 where it requires administrative
privileges to install. I do not have windows 2007 so I cannot confirm
this (if someone has windows a spare 2007 or want to sponsor this
platform get in touch with me). A few of the highlights:

     * Improved installer * A lot of bugfixes and improvements * Serious memory leak fixed * Added a few new options to NSCA module * New service name and description * Improved CHeckFile2 (new option max-dir-depth, path, pattern) * Added support for changing name and description of service from the /install command line * Added more filter operators to all numeric filters so they accept eq:, ne:, gt:, lt: in addition to =, >, <, <>, !, !=, in: (#269) * Added better support for numerical hit matching in the eventlog module. You can now use exact and detailed matching. * Cleaned up the checkProcState code and it is not a lot better. * Added new option 16bit to checkProcState. When set checkProcState will enumerate all 16 bit processes found running under NTVDM. * Added new command line options pdhlookup and pdhmatch (to CheckSystem) to lookup index and names. * Added new module A_DebugLogMetrics.dll which can be used to generate debug info. * Brand new build environment based upon boost build!!! * Modified /about so it now shows a lot of useful(?) info. 

For all changes refer to the changelog. On a side not I will during the
night switch over to a new host so hopefully the site will be more
stable as well! // Michael Medin

Title: 0.4.1 RC3
Author: mickem
Tags: release-candidate
Status: published

Yet another RC (0.4.1.66) which hopefully fixes the check\_nt crash some
people was experiencing. If not please urgently send crash dumps and let
me know! Also introduces some new minor features as well as bug fixes:
Full change log:

     2012-11-18 MickeM * Created nscpnobp.exe which is a version without break pad for older machines (windows 2000 and nt4). This can only be foundin the zip file (not the msi) * Added some missing file to zip * Removed counters.defs since it is not used anymore 2012-11-17 MickeM * CheckEventLog: Added debug message lisgin all loaded filters to make it simpler to detect missing once * SimpleCache: Added keywords not-found-msg and not-found-code option to configure the outcome of "item not found". check_cache index=foobar "not-found-code=Doch! item was not found" not-found-code=critical * CheckProcess is no longer case sensetive * CheckServiceState: added support for pending states 2012-11-16 MickeM * CheckDriveSize now supports regular expressiion filtering: CheckDriveSize ShowAll MaxWarn=1M MaxCrit=2M CheckAll=volumes matching=.*[CD].* 2012-11-15 MickeM * CheckFiles filter is now optional (not specifying a filter will find all files matching) * CheckFiles no longer matching . and .. 2012-11-14 MickeM * Added perf-unit to allow for stable performance data units (if not specified it will guess which is the current solution). checkmem type=paged MaxWarn=80% perf-unit=M => 'paged bytes %'=34%;80;0 'paged bytes'=8454.04M;19629.84;0;0;24537.3 checkmem type=paged MaxWarn=80% perf-unit=K => 'paged bytes %'=34%;80;0 'paged bytes'=8655200K;20100963.19;0;0;25126204 checkmem type=paged MaxWarn=80% perf-unit=B => 'paged bytes %'=34%;80;0 'paged bytes'=8872108032B;20583386316;0;0;25729232896 checkmem type=paged MaxWarn=80% => 'paged bytes %'=34%;80;0 'paged bytes'=8.25G;19.1;0;0;23.96 * Fixed threadding issue related to servers (ie. check_nt causing a crash) Dont know what I was thinking when I designed that, pretty stupid bug :( 

// Michael Medin

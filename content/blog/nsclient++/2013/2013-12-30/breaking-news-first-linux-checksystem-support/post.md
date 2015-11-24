Title: Breaking news: First linux CheckSystem support...
Author: mickem
Tags: 0.4.2, linux, release-candidate
Status: published

Yaaaay...\
 First sign of Linux Love for CheckSystem:

The short version:

    mickem@debian-x64:/mnt/nscp/build/lin-cdt$ ./nscp test
    D       core NSClient++ 0,4,2,72 2013-12-23 unknown Loading settings and
    ...
    load CheckSystemUnix
    D       core adding /mnt/nscp/build/lin-cdt/modules/libCheckSystemUnix.so
    check_uptime show-all
    L     client OK: uptime: 3d 11:8h, boot: 2013-Dec-27 06:26:27 (UTC)
    L     client  Performance data: 'uptime_uptime'=299296;172800;86400
    ...
    Linux debian-x64 3.2.0-4-amd64 #1 SMP Debian 3.2.51-1 x86_64 GNU/Linux
    mickem@debian-x64:/mnt/nscp/build/lin-cdt$

The slightly longer version:

    mickem@debian-x64:/mnt/nscp/build/lin-cdt$ ./nscp test
    D       core NSClient++ 0,4,2,72 2013-12-23 unknown Loading settings and logger...
    D   settings No entries found looking in (adding default): /mnt/nscp/build/lin-cdt/boot.ini
    D   settings No valid settings found (tried): old://${exe-path}/nsc.ini, ini://${shared-path}/nsclient.ini
    E   settings Settings contexts exhausted, will create a new default context: ini://${shared-path}/nsclient.ini
                        /mnt/nscp/master/nscp/helpers/settings_manager/settings_manager_impl.cpp:183
    D   settings Creating instance for: ini://${shared-path}/nsclient.ini
    L   settings Configuration file not found: /mnt/nscp/build/lin-cdt/nsclient.ini
    D       core NSClient++ 0,4,2,72 2013-12-23 unknown booting...
    D       core Booted settings subsystem...
    D       core booting::loading plugins
    D       core NSClient++ - 0,4,2,72 2013-12-23 Started!
    L     client Enter command to inject or exit to terminate...
    load CheckSystemUnix
    D       core adding /mnt/nscp/build/lin-cdt/modules/libCheckSystemUnix.so
    check_uptime show-all
    L     client OK: uptime: 3d 11:8h, boot: 2013-Dec-27 06:26:27 (UTC)
    L     client  Performance data: 'uptime_uptime'=299296;172800;86400
    exit
    L     client Exiting...
    D       core Attempting to stop all plugins
    D       core Stopping all plugins
    D       core Unloading plugin: libCheckSystemUnix.so...
    D       core Stopping: Settings instance
    mickem@debian-x64:/mnt/nscp/build/lin-cdt$ uptime
     18:34:51 up 3 days, 11:08,  4 users,  load average: 0.23, 0.86, 0.90
    mickem@debian-x64:/mnt/nscp/build/lin-cdt$ uname -a
    Linux debian-x64 3.2.0-4-amd64 #1 SMP Debian 3.2.51-1 x86_64 GNU/Linux
    mickem@debian-x64:/mnt/nscp/build/lin-cdt$

// Michael Medin

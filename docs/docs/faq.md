# FAQ:  Frequently Asked Questions

## I am having problems where do I start?

NSCP has a built-in "test and debug" mode that you can activate with the following command `nscp test`

What this does is two things.

1. it starts the daemon as "usual" with the same configuration and such.
2. it enables debug logging and logs to the console.
   This makes it quite easy to see what is going on and why things go wrong.

## MSI or ZIP installation?

In general never use the ZIP installation unless you have a strong reason for doing so.
The MSI is the preferred way to install NSClient++ and will work much better then trying to manually install it.

## Failed to open performance counters

- The first thing to check is the version. If you are using an old version (pre 0.4.2) upgrade!
  In 0.4.2 PDH was greatly improved and all core checks stopped using PDH which means that for "normal" checks you no
  longer need PDH.
- Second thing to check is whether the servers' performance counters working?
  Sometimes the performance counters end up broken and need to be rebuilt there is a command to validate performance
  counters: `nscp sys --validate`

For details: Microsoft KB: [http://support.microsoft.com/kb/300956](http://support.microsoft.com/kb/300956) essentially
you need to use the `lodctr /R` command.

## Bind failed

Usually this is due to running more than one instance of NSClient++ or possibly running another program that uses the
same port.

- Make sure you don't have any other instance NSClient++ started.
- Check if the port is in use (`netstat -a` look for LISTENING)

## I get <insert random error from Nagios here>

Errors coming from Nagios are often not related to errors inside NSClient++.
As most protocols supported by Nagios does not support reporting errors only statuses.
To see the error do the following:

```
net stop nscp
nscp test --log trace
... wait for errors to be reported ...
exit
net start nscp
```

## High CPU load and `check_eventlog`

Some people experience high CPU load when checking the event log this can usually be resolved using the new command line
option scan-range setting it to the time region you want to check

`check_eventlog ... scan-range=12h ...`

## Return code of 139 is out of bounds

This means something is wrong. To find out what is wrong you need to check the NSClient++ log file.
The message means that an plugin returned an invalid exit code and there can be many reasons for this but most likely
something is miss configured in NSClient++ or a script your using is not working.
So the only way to diagnose this is to check the NSClient++ log.

One simple way to show the log is to run in test mode like so:

```
net stop nscp
nscp test
... wait for errors to be reported ...
exit
net start nscp
```

## How do I enable debug log

By default, the log level is info which means to see debug messages you need to enable debug log:

```
[/settings/log]
file name = nsclient.log
level = debug
```

## How do I properly escape spaces in strings

When you need to put spaces in a string you need to make sure you escape them properly in the Nagios config.
As usually you can do it anyway you like, but I prefer: `check_nrpe ... 'this is a string'`

## How do I properly escape $ in strings

Dollar signs are "strange" in Nagios and has to be escaped using double $$s. 
Thus in Nagios config you need to put `$$`.

## How do I properly escape \ in strings

Backslashes and some other control characters are handled by the shell in Nagios and thus escaped as such.

| Location   | Escape character |
| ---------- | ---------------- |
| Nagios     | ...\\...         |
| NSClient++ | ...\\...         |

## Arguments via NRPE

For details see [external script](howto/external_scripts.md#arguments)

## Nasty metacharacters

If you get illegal metachars or similar errors you are sending characters which are considered harmful through NRPE.
This is a security measure inherited from the regular NRPE client.

The following characters are considered harmful: \|\`&><'\"\\[]{}
To work around this you have two options.

1. You can enable it
2. You can switch most commands to not use nasty characters

To enable this in the NRPE server you can add the following:

```
[/settings/NRPE/server]
allow nasty characters=true

[/settings/external scripts]
allow nasty characters=true
```

To not use nasty characters you can replace man y of them in built-in commands:

| Expression | Replacement |
| ---------- | ----------- |
| >          | gt          |
| <          | lt          |
| '          | str(...)    |
| ${..}      | %(..)       |

## Rejected connection from: your IP address here

This is due to invalid configuration.
One important thing you **NEED** to configure is which hosts are allowed to connect. If this configuration is missing
or invalid you will get the following error:

```
2013-04-02 16:34:07: e:D:\source\nscp\trunk\include\check_nt/server/protocol.hpp:65: Rejected connection from: ::ffff:10.83.14.251
```

To resolve this please update your configuration:

```
[/settings/default]

; ALLOWED HOSTS - A coma separated list of hosts which are allowed to connect. You can use netmasks (/ syntax) or * to create ranges.
allowed hosts = 10.11.12.0/24
```

## Timeout issues

Configuring timeouts can some times be a problem and cause strange errors.
It is important to understand that timeouts are cascading this means if you have all timeouts set to 60 seconds they
will all miss fire.

The Nagios server timeout will fire after exactly 60 seconds but the script timeouts will be started maybe 1 second
after the Nagios service check timeout this means once we reach 60 seconds the Nagios service timeout will fire first
and 1 second after the script will timeout. This you always have to set each timeout slightly less to accommodate this
drift.

If your command takes 60 seconds you need to set the timeouts like this:

### 1. Script timeout: 60s

```
[/settings/external scripts/wrappings]
vbs = cscript.exe //T:120 //NoLogo scripts\\lib\\wrapper.vbs %SCRIPT% %ARGS%
```

### 2. External script timeout: 65 seconds

```
[/settings/external scripts]
timeout = 65
```

### 3. NRPE/server timeout: 70s

```
[settings/NPRE/server]
timeout = 70
```

### 4. check_nrpe timeout: 75s

```
check_nrpe -t 75
```

### 5. Nagios service check timeout: 80s

```
service_check_timeout=80
```

## How do I rotate log files

```
[/settings/log]
date setting = %Y.%m.%d %H:%M:%S
file name = nsclient.log
level = info

[/settings/log/file]
max size = 2048000
```

## What's the difference between `CheckFoo` and `check_foo`

In older version of NSClient++ (pre 0.4.1) there were only `CheckFoo` type commands so they where
called `CheckCPU` `CheckMem` `CheckProcess` etc etc...
In 0.4.2 we introduced a new set of commands which were more generic and similar and they are
called `check_cpu` `check_memory` `check_process` etc etc..
The previous ones are only for compatibility and will eventually be removed from NSClient++.
Currently they are about 90% compatible which means some things will not work as before and some commands are not even
present anymore.

1. personally think that the benefit of using the new commands makes the effort required to convert it worth it but if
   you have a specific command using the old syntax which no longer work please do let me know and I will see about
   adding support for it.
2. `check_nt`

## I use check_nt and...

Check_nt is NOT a good protocol and is considered abandon-ware as noone updates the check_nt command any longer.
NSClient++ supports it only for legacy reasons.
There is generally no reason to use `check_nt` as `check_nrpe` and `check_nscp` can achieve the same thing.

## MEMUSE reports the wrong value

No it does not :)
MEMUSE reports physical+page (normally called committed bytes). This is the amount of memory the system has promised to
various applications.
Thus it will be "more" than your RAM if you want to check physical memory please use `check_nrpe` and `check_memory`
instead.

## I use severity but still don't get errors (or get non error messages).

This is a "feature" of the Windows Event-log API. They have something called severity which most programs do not use as
severity.
instead please try using level which is more accurate. This is less relevant in "modern Windows"  where severity has
been removed.

## What is insecure mode with NRPE

The NRPE protocol is broken it is using some strange encryption protocols which are (to our knowledge) rather insecure.
To work around this in 0.4.x we introduced real SSL support as well as certificate based authentication. This became the
default in 0.4.3.

To allow old "legacy" `check_nrpe` connect to NSClient++ you need to enable *insecure mode* which can be done in
multiple ways.

1. In the MSI installer there is an option to select insecure mode
2. From command line you can run the `nscp nrpe install --insecure`
3. You can manually set the option in your config file

All these options will result in the following configuration:

```
[/settings/NRPE/server]
certificate key =
certificate = ${certificate-path}/certificate.pem
ssl options =
allowed ciphers = ADH
ssl = true
insecure = true
```

If you instead opt to use the more secure standard SSL approach used in NSClient++ you can easily install NSClient++ on
a Linux system as well.


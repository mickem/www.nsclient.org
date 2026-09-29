---
date:
  created: 2026-09-29
---

# 0.24.0 Host facts, NSClient++ on macOS, and new checks from Active Directory to Kubernetes

0.24.0 is a big release, and most of it is about the agent knowing more: what
the host it runs on actually is, and what the services on it are doing.

The headline is **host facts** — an opt-in inventory the agent keeps about its
host. The OS and hardware, network interfaces, volumes, installed software,
services, scheduled tasks, Docker, MySQL, SQL Server and Hyper-V each become a
fact set you turn on in the module that already checks that thing. The
collected document is served over REST behind two new grants, shown on a new
*Facts* page in the web UI, available as `facts` in `nscp test`, and uploaded
to the fleet server by an enrolled agent — as a hash on every poll, and as the
document only when the server says it holds a different one. Every set is off
until you enable it.

Alongside that, NSClient++ runs on **macOS** for the first time (an
experimental Apple silicon package, with `CheckSystem` ported to Darwin), and
there is a wave of new, experimental checks: Active Directory, Hyper-V,
Kubernetes, Windows Failover Clusters, NPS and RADIUS, domain registration
expiry, and eight more SQL Server checks.

The hardening pass continues. One request can no longer cost the agent without
bound — command nesting, `check_multi` fan-out, regular-expression matching and
log-file reads all have limits now. The shared default password is stored hashed,
`nscp web install` sets up HTTPS on its own, a module can only be named by a
file name, the Linux service runs sandboxed under its own group, every DLL the
Windows installer ships is signed, and a failing background thread can no
longer take the whole agent down. Several of these have an upgrade note worth
reading — `NSCAServer` users in particular.

## ✨ Highlights

- 🏷️ **Host facts: an opt-in inventory of the host.** `os`, `hardware`,
  `network.interfaces`, `storage.volumes`, `software.installed`,
  `services.installed`, `tasks.scheduled`, `agent`, `docker`, `mysql`,
  `mssql` and `hyperv.vms` sets, each produced by the module that already
  checks it and each off until enabled. CheckSystem also publishes three new
  selector tags — `os_family`, `arch` and `virtualization` — that mean the same
  thing on every platform. (#1559, #1583, #1589, #1594)
- 📤 **Facts over REST, in the web UI and on the fleet server.**
  `GET /api/v2/facts` and `POST /api/v2/facts/commands/refresh` sit behind the
  new `facts.get` and `facts.refresh` grants, which only the `full` role
  carries. An enrolled agent uploads its document only when the server's hash
  differs. (#1559, #1590)
- 🍎 **NSClient++ on macOS.** An experimental, self-contained Apple silicon
  `.pkg` and `.tar.gz`, running as a launchd daemon. `CheckSystem` carries all
  21 of its Linux commands on macOS, with `check_service` checking launchd
  jobs. The package is not signed or notarized yet. (#1578, #1593)
- 🧪 **New experimental modules: `CheckActiveDirectory`, `CheckHyperV` and
  `CheckKubernetes`.** AD replication, the machine secure channel and a real
  Kerberos probe of each KDC; Hyper-V host capacity, hypervisor CPU and
  per-VM health; and a Kubernetes cluster's API, pods, nodes and workloads,
  read over HTTPS with a service-account token and no `kubectl`. (#1601,
  #1586, #1587)
- 🪟 **More Windows server checks.** Failover Cluster groups, resources,
  nodes and networks that follow a role across nodes; NPS authentication,
  accounting and counters; and eight new SQL Server checks — availability
  groups, blocking, counters, integrity, sessions, tempdb, transactions and
  waits. (#1600, #1598, #1398)
- 🌐 **`check_domain` and `check_radius` in CheckNet.** Domain registration
  expiry over RDAP with an optional WHOIS fallback, and an authenticated RADIUS
  probe that validates the response authenticator and reads its credentials
  from a protected file. (#1599, #1598)
- 🛡️ **Bounded work per request.** A deeply nested `check_multi` could
  exhaust a thread's stack, a backtracking regular expression could pin a
  worker for minutes, and `check_logfile` could read a whole multi-gigabyte
  file into memory — each reachable by any caller allowed to pass arguments.
  Nesting stops at 16 levels, `check_multi` at 128 commands, regex matching at
  30 s per check, and `check_logfile` reads at most `max-size` (64 MiB) per
  call. (#1554)
- 🔒 **The shared default password is stored hashed**, and `NSCAServer` no
  longer inherits it. `NSCAClient` — how almost everyone uses NSCA — is
  unaffected, but a host that *receives* NSCA through `NSCAServer` with the key
  in `/settings/default` must move the key before upgrading. A new
  `nscp nsca install` sets either side. (#1567)
- 🔐 **Hardening across the agent.** `nscp web install` serves HTTPS and
  generates its certificate; a `[/modules]` entry must be a file name; settings
  are never migrated *to* a remote store; credential-looking keys are redacted
  even for unloaded modules; the Linux unit is sandboxed under
  `Group=nsclient`; every shipped Windows DLL is Authenticode-signed; and a
  worker thread that throws is contained and logged instead of ending the
  process. (#1553, #1577, #1582, #1584)

## 🔍 Detailed changes

### 🏷️ Host facts

A tag selects a group of hosts; a fact describes one. The agent has published
a handful of tags for a while (`os_name`, `os_version`, a tag per running
service), but it knew a good deal more about the machine — every value below is
read by one of its checks — and published none of it. So nothing could tell a
64-core Linux VM from a laptop without running a check against the host.

Facts are an inventory the core keeps: each producing module contributes fact
sets, the core assembles them into one document, and the document is re-read
on a schedule, on a settings reload, or on demand. **Every set is off by
default** — an inventory is data an operator did not necessarily agree to ship
— and is turned on in the module that produces it:

```ini
[/settings/system/windows/facts]   ; [/settings/system/unix/facts] on Linux and macOS
os = true
hardware = true
network.interfaces = true
software.installed = true
services.installed = true

[/settings/disk/facts]
storage.volumes = true

[/settings/facts]
agent = true
```

| Set | Produced by | Describes |
|---|---|---|
| `os` | CheckSystem | family, name, version, arch, virtualization, domain |
| `hardware` | CheckSystem | manufacturer, model, CPU cores, memory |
| `network.interfaces` | CheckSystem | per interface: MAC, status, speed, addresses |
| `software.installed` | CheckSystem | per program: version, publisher, architecture, source, install date, size |
| `services.installed` | CheckSystem | Windows services or systemd units, stopped and disabled included, with their startup type |
| `storage.volumes` | CheckDisk | per volume: device, filesystem, type, label, size |
| `tasks.scheduled` | CheckTaskSched | every scheduled task, hidden and disabled included |
| `docker`, `docker.containers`, `docker.images` | CheckDocker | the daemon, its containers and images |
| `mysql`, `mysql.databases` | CheckMySQL | the server and its databases |
| `mssql`, `mssql.databases` | CheckMSSQL | the instance and its databases |
| `hyperv.vms` | CheckHyperV | per VM: GUID, generation, configured processors and memory, checkpoints, replica role |
| `agent` | the core | version, loaded modules, whether it is enrolled |

A few rules hold across all of them. A record's `id` is the name the matching
check already uses for that instance — a `storage.volumes` id is what
`check_drivesize` calls `drive`. A field that could not be determined is
omitted, never written empty, so an absent key means unknown. The sets describe
the host, not how busy it is: no free space, traffic, container state, uptime
or connection counts, which change every round and belong to the checks. No set
carries a login, a password or a command line. A list stops at 2500 records and
says so under `errors`, and a set that cannot be read keeps its last good value
and reports why. Sets that talk to a service (Docker, the databases, Hyper-V,
services and tasks) are never read on the startup round, so a daemon that does
not answer cannot hold up the service start.

CheckSystem also publishes three new **tags** at start — `os_family`, `arch`
and `virtualization` — with one vocabulary on every platform (Windows' `AMD64`
is published as `x86_64`), so one fleet selector covers a mixed fleet.
`virtualization` reads `none` on a Windows host that runs Hyper-V, WSL2 or
virtualization-based security itself: what the firmware says outranks the
hypervisor bit.

**Reading them.** `nscp test` gains `facts` and `facts refresh`. The web UI
gains a *Facts* page that shows the document and turns a set on through the
settings API. Over REST, `GET /api/v2/facts` returns the document (or one
subtree with `?path=os`) and `POST /api/v2/facts/commands/refresh` collects a
round now. Both need new grants, `facts.get` and `facts.refresh`, which only
the built-in `full` role carries; add `facts.get` to a role that should read the
inventory. See [Host Facts](https://nsclient.org/docs/concepts/facts/).
(#1559, #1583, #1589, #1594)

### 📤 Fleet — facts leave the host only when the server lacks them

An enrolled agent now reports the SHA-256 of its facts document on every
desired-state poll and state report, and uploads the document itself to
`POST /agent/v1/facts` only when the server's `X-Facts-Hash` answer differs.
A server that never sends that header is never sent the document. Uploads back
off from one minute to an hour on rejection, honour `Retry-After`, and are held
for a day after a 413, with the log naming the largest sets. With no set
enabled, only the hash of the empty document goes out. To keep a set on the
host but off the server, turn it off or do not enroll the host. (#1590)

The fleet trust model is tightened too: a renewal can no longer rotate the
bundle signing key unless the new key is signed by the old one, and the fleet
guide now states plainly that a fleet server is an administrator of every host
enrolled with it.

### 🍎 macOS

Releases now carry `NSCP-<version>-macos-arm64.pkg` and a matching `.tar.gz`.
Both bundle their libraries, so the target Mac needs no Homebrew. The `.pkg`
installs under `/usr/local`, creates a hidden `_nsclient` account and registers
a launchd daemon:

```bash
sudo installer -pkg NSCP-<version>-macos-arm64.pkg -target /
sudo launchctl print system/com.nsclient.nscp          # status
sudo launchctl kickstart -k system/com.nsclient.nscp   # restart
sudo /usr/local/sbin/uninstall-nsclient --purge        # remove
```

It is experimental in the sense a young check is: it works, but the layout,
account and launchd job may still change. It is **Apple silicon only**, and
**not signed or notarized** — install from a terminal, or clear the quarantine
flag first. `CheckDisk` and `CheckLogFile` are not in the macOS build yet.

`CheckSystem` runs on macOS with the same commands, keywords and settings
section (`/settings/system/unix`) as on Linux, reading sysctl, Mach, libproc,
IOKit and `launchctl` instead of procfs. A value macOS does not have is reported
as absent — the keyword renders `unknown` and emits no perfdata — or the check
returns UNKNOWN, never an unmeasured zero. `check_service` checks launchd jobs
by label, `check_installed_software` lists receipts, app bundles and Homebrew
kegs, and `check_os_updates` gains `live=true` to ask Apple's update server.
(#1578, #1593)

### 🧪 New modules

| Module | Commands | What it covers |
|---|---|---|
| `CheckActiveDirectory` (Windows) | `check_ad_replication`, `check_secure_channel`, `check_kdc` | Inbound replication links on a DC; the machine secure channel via netlogon; a real Kerberos AS-REQ to each KDC, so a KDC that accepts connections but issues no tickets is caught |
| `CheckHyperV` (Windows) | `check_hyperv_host`, `check_hyperv_cpu`, `check_hyperv_vms` | VM health summary and hypervisor capacity; logical processor load the ordinary CPU counters cannot see on a host; per-VM state, heartbeat, memory, checkpoints and Replica status |
| `CheckKubernetes` | `check_kubernetes`, `check_pods`, `check_nodes`, `check_workloads` | API readiness and node counts; the `kubectl get pods` STATUS column; node pressure and cordons; desired versus available replicas |

All three are off by default and marked experimental: their options, keywords
and output may still change. `CheckKubernetes` is configured once under
`[/settings/kubernetes]` (an API server and token, a JSON kubeconfig, or nothing
when running in-cluster); no check takes a `url=` or `token=`, so a REST caller
cannot redirect the token elsewhere. Building it from source needs Boost 1.77
or later. See the [Active Directory](https://nsclient.org/docs/scenarios/active-directory/)
and [Kubernetes](https://nsclient.org/docs/scenarios/kubernetes/) scenarios.
(#1601, #1586, #1587)

### 🪟 Windows server checks

**Failover Clusters.** `CheckWindowsApps` gains `check_cluster_groups`,
`check_cluster_resources`, `check_cluster_nodes` and `check_cluster_networks`.
They read the local cluster through ClusAPI — no PowerShell or WMI — include
objects owned by other nodes, and never move or restart anything. A clustered
role is followed when it moves; an ownership change alone stays OK. A missing
cluster, an access error or a partial read is UNKNOWN, never an empty OK. An
offline or failed group is CRITICAL by default, so a role that is offline on
purpose alerts until you filter it out (`name=SQL` selects the ones you
expect). ClusAPI is loaded on demand, so a host without clustering is
unaffected. (#1600)

**NPS.** `check_nps_auth`, `check_nps_accounting` and `check_nps_counters`
cover a Network Policy Server's authentication outcomes, accounting and
performance counters. (#1598)

**SQL Server.** `CheckMSSQL` gains eight checks, all on the module's existing
connection settings:

| Command | Watches | Rights |
|---|---|---|
| `check_mssql_sessions` | session and connection counts per database and login | `VIEW SERVER STATE` |
| `check_mssql_blocking` | blocked sessions and blocking chains | `VIEW SERVER STATE` |
| `check_mssql_transactions` | old or leaked open transactions, long-running requests | `VIEW SERVER STATE` |
| `check_mssql_counters` | buffer cache, page life expectancy, batch and lock rates | `VIEW SERVER STATE` |
| `check_mssql_waits` | wait statistics by category, scheduler pressure | `VIEW SERVER STATE` |
| `check_mssql_tempdb` | tempdb space by consumer, volume headroom | `VIEW SERVER STATE` |
| `check_mssql_availability_groups` | Always On replica and database health | `VIEW SERVER STATE` |
| `check_mssql_integrity` | suspect pages, age of the last successful `CHECKDB` (never runs it) | `SELECT` on `msdb.dbo.suspect_pages`; `sysadmin` for `checkdb_age` |

A missing permission degrades a keyword to a sentinel or returns UNKNOWN
rather than raising an alert. `check_mssql_databases` gains `data_headroom`
and `log_headroom` — how far a database can grow before it hits a file's
`max_size` or fills the volume it grows into, with files on one volume sharing
its free space:

```
check_mssql_databases "critical=data_headroom < 1G and data_headroom >= 0"
```

And one fix for every check: an integer keyword compared against a size is no
longer routed through a floating-point number, so values above 2^53 bytes
compare exactly. (#1398)

`CheckWindowsApps` and `CheckMSSQL` are experimental modules, so all of the
above may still change in options, keywords and output.

### 🌐 CheckNet — domain expiry and RADIUS

`check_domain` watches a domain's registration expiry the way
`check_certificate` watches a certificate's, warning below 30 days and critical
below 10 by default. It queries RDAP over verified HTTPS, prefers the
registrar's date over the registry's, and can fall back to an explicitly named
WHOIS server:

```
nscp client --module CheckNet --boot --query check_domain domain=example.com
```

It makes a live request on every run, so schedule it daily from one place per
domain. The default endpoint is the public `https://rdap.org` redirector, which
means the domain you check is sent to a third party; `rdap-url=` names a
provider of your choice. WHOIS is unencrypted and the fallback also applies
after a TLS failure, so enable it only with a server you trust.

`check_radius` sends a PAP authentication, an expected rejection, or (when
enabled) a Status-Server probe, validates both response authenticators, and
reads its shared secret and credentials from files that must be protected.
Both commands are experimental. (#1599, #1598)

### 🛡️ Resource limits on one request

Three costs were unbounded, each reachable from one request by a caller that
may pass arguments to a check — an NRPE peer with `allow arguments = true`, or
a REST caller with `queries.execute`.

| Limit | Value | Past it |
|---|---|---|
| Command nesting depth | 16 | The query is refused with a structured error. `check_multi`, `check_and_forward` and `check_timeout` re-enter the core on the same thread, and a few thousand levels exhausted the stack — not a catchable failure on Windows. |
| `check_multi` commands per call | 128 | UNKNOWN, naming the count. |
| Regular-expression matching | 30 s per check, 1 MiB per subject | Further matches are refused and the check returns UNKNOWN rather than quietly under-matching. A catastrophic-backtracking pattern no longer pins a worker for the length of an event log, and its failure is no longer misreported as "invalid syntax". |

Compiled patterns are now cached, so ordinary filters get faster.
`check_logfile` gains `max-size` (default `64m`): with a bookmark it paces the
read and nothing is lost; without one a larger file is UNKNOWN rather than
silently half-read — add `bookmark=auto`, `max-lines`, or raise `max-size`.
(#1554)

### 🔒 The shared default password, and NSCA's own key

`nscp web install` and `nscp web password --set` now store
`/settings/default/password` as a `pbkdf2-sha256$…` hash, and the Windows
installer hashes a password it is given. The web UI and check_nt verify
against either form, so a clear-text value you wrote by hand keeps working;
`nscp web password --set <the same value>` hashes it in place. `--display`
cannot show a hashed password any more.

NSCA does not verify a password — it encrypts with it — so it could never use
a hash. `NSCAServer`, the listener that *receives* NSCA, therefore no longer
reads the shared section, and refuses to start with encryption on and no key.
Only a start refuses: `nscp settings`, `nscp client --module NSCAServer` and
the documentation build still load the module without its listener, so the
section can be listed and fixed in place.
`NSCAClient`, which *submits* to an NSCA daemon, always had its key on the
client target and is unaffected. A new command sets either side:

```commandline
nscp nsca install --host <nsca-server> --password <key> --encryption aes256   # submit
nscp nsca install --server --password <key>                                   # receive
```

The Windows installer takes the same values as `NSCA_SERVER`, `NSCA_PORT`,
`NSCA_PASSWORD`, `NSCA_ENCRYPTION` and `NSCA_HOSTNAME`. (#1567)

### 🛡️ Hardening

- **`nscp web install` serves HTTPS by default** and generates a self-signed
  certificate when none exists, instead of blanking the certificate and leaving
  a web server that refused to start. On Linux a generated certificate is handed
  to the service account. `--insecure` asks for plain HTTP on port 8080. (#1584)
- **A module is named by a file name.** A `[/modules]` entry or `Control.LOAD`
  that is a path — absolute, or walking out with `..` — is refused; naming a
  module was also naming any file on the host. The `./modules` fallback resolves
  against `${exe-path}`. (#1553)
- **Settings are never migrated *to* an `http(s)://` store**, which would send
  every credential in the configuration to whatever the URL names. Importing
  from one is unchanged. (#1553)
- **Credential-looking keys are redacted whether or not their module is
  loaded.** `GET /api/v2/settings` and `nscp settings --list` used to print a
  password left behind for a disabled module in clear. (#1553)
- **The Linux systemd unit is sandboxed** (`UMask=0027`, `ProtectKernel*`,
  `ProtectControlGroups`, `RestrictSUIDSGID`, `RestrictRealtime`,
  `LockPersonality`) and runs under `Group=nsclient`, which closes a disclosure
  on Debian/Ubuntu where runtime files were readable by `nogroup`.
  `ProtectSystem`, `ProtectHome`, `PrivateTmp` and `NoNewPrivileges` are
  deliberately left out because they change what disk and mount checks report,
  or break `sudo` in scripts; the unit explains why. The DEB no longer depends
  on `sudo`, and `CauseCrashes` is no longer shipped. (#1553)
- **A worker thread that throws is contained.** Every background thread now
  starts with a guard, so an exception that escapes it is logged as
  `Thread '<name>': terminated by an uncaught exception: …` instead of calling
  `std::terminate()` on the whole agent. No crash of this kind has been
  reported — most bodies already caught — but the guard is now structural
  rather than per-site. `nsclient.fatal` lands next to `nsclient.log`. (#1577)

### 📦 Packaging and supply chain

Every DLL the Windows installer ships — modules, NSClient++ libraries and
bundled third-party libraries — is now Authenticode-signed like `nscp.exe`, so
an AppLocker or App Control publisher rule covers them. Signing credentials are
only available to the release build. Each Windows release publishes a
CycloneDX 1.6 SBOM (`NSCP-<version>-<platform>.cdx.json`, and `sbom.cdx.json`
plus `SHA256SUMS` inside the zip), every release asset is attested
(`gh attestation verify <file> --repo mickem/nscp`), and every third-party
download the build makes is checked against a recorded digest or commit before
use. (#1581, #1582)

### 🐛 Bug fixes

- **Perfdata no longer reports a missing threshold as `0`.** `'time'=2ms;1000;0`
  read as "critical above 0" in PNP4Nagios, Grafana and Icinga; an unbounded
  field is now left empty (`'time'=2ms;1000`).
- **`check_cpu` answers from the samples it has.** For the first minutes after a
  start or a settings reload, a `5m` window averaged real samples with empty
  slots, so a saturated host read as idle. Before the very first sample it now
  answers UNKNOWN; on Linux `check_memory` and `check_pagefile` do the same.
- **Per-core CPU numbers are right on hosts with more than ten cores.** Core 10
  and up were reported under the wrong numbers in `check_cpu`, the real-time
  filters and the per-core metrics.
- **A settings reload no longer piles things up.** `LUAScript` and
  `DotnetPlugins` unload the previous generation instead of leaking it and
  registering every command again; `CheckHelpers` drops removed aliases;
  `SimpleFileWriter` stops appending its syntax once per reload; and
  `CheckMKClient`/`CheckMKServer` release their previous Lua scripts. (#1565)
- **A reload requested from inside a check is applied after the check
  returns.** A Lua check served over NRPE that reloaded the service restarted
  the NRPE listener from one of its own threads, and `check_nrpe` timed out from
  then on. The reload is now handed to the scheduler.

## ⚠️ Upgrade notes

- 🔒 **If you run `NSCAServer` (the NSCA *listener*) and its key came from
  `/settings/default/password`, set it under `[/settings/NSCA/server]` before
  upgrading**, or with `nscp nsca install --server --password <key>`. Otherwise
  the module refuses to start. `NSCAClient` is unaffected.
- **A `check_logfile` that reads a file over 64 MiB without a bookmark now
  returns UNKNOWN.** Add `bookmark=auto`, `max-lines`, or raise `max-size`. A
  `check_multi` running more than 128 commands must be split.
- **`nscp web password --display` cannot show a hashed password.** Tooling that
  read the shared password back out of `nsclient.ini` now sees a
  `pbkdf2-sha256$…` string.
- **A `[/modules]` entry that is a path rather than a file name is refused.**
  Move the module into the module folder and name it.
- **Settings dumps show `***`** for every key whose name reads as a credential,
  including those of modules that are not loaded.
- **On Linux, external scripts inherit the service's `UMask=0027`.** A script
  that writes a file for another account to read should set the mode itself. If
  you created the service account by hand, make sure an `nsclient` group exists.
  If a script escalates with `sudo`, keep the package installed — the DEB no
  longer pulls it in.
- **If you alert on the agent process disappearing**, a dying worker thread no
  longer ends the process. Alert on the log line
  `Thread '<name>': terminated by an uncaught exception` instead.
- **A fleet renewal can no longer rotate the signing key unendorsed.** A host
  whose server rotated its key without signing the new one with the old must be
  re-enrolled.
- **Enabled fact sets on an enrolled host now reach the fleet server.** Nothing
  is sent while no set is enabled, which is the default.
- **Give `facts.get` to any non-admin web role that should read the
  inventory**; only the `full` role carries it.
- **If you parse the warn/crit fields of perfdata yourself**, treat an empty
  field as "no threshold" rather than expecting `0`.
- **A script that calls `core.reload(...)` from inside a check** and reads its
  settings straight after should read them a moment later: the reload now
  applies after the check returns.
- **A custom check_mk Lua script with an unload hook** now sees it run on every
  settings reload, not only at shutdown.

Security notices for this release are on the
[security notices page](https://nsclient.org/docs/security/notices/), and the
full list of behaviour changes is on the
[upgrading page](https://nsclient.org/docs/setup/upgrading/).

## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.24.0){ .md-button }

// Michael Medin

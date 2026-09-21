---
date:
  created: 2026-09-20
---

# 0.22.0 Metrics a scraper can actually read, Mod-Gearman without an open port, and a much smaller install

0.22.0 rebuilds the metrics side of the agent. `/api/v2/openmetrics` served the
JSON keys verbatim — names with dots, spaces and colons in them, no types, no
help text, six significant digits — which a strict parser rejected outright.
It now serves a conformant, self-describing OpenMetrics document: every family
named to the grammar, typed, described, carrying its unit, and per-instance
readings collapsed into one family with a `core`, `nic` or `drive` label
instead of one family per core. Every metric name changes, so read the upgrade
note before you upgrade a scraped host.

The second theme is a new transport. `GearmanClient` makes the agent a
Mod-Gearman worker: a Naemon or Nagios Core keeps scheduling its checks, the
agent pulls them off a `gearmand` job server and answers them as native
queries, and the monitored host needs no inbound port at all. The same module
submits passive results back into the core's result queue. It ships marked
**experimental** and has not been exercised at scale: it is verified end to end
against a real job server on both cores, but no one has yet run it across a
large estate, so put it on a slice of your hosts before you move a whole
Mod-Gearman installation onto it.

Then a long tail of security work — the low-severity tier of the audit, in
three parts, plus a second undefined-behaviour sweep and the ten worst
threading bugs — and a packaging release: common code moved out of every
plugin into shared libraries, Windows ARM64 is back, and there is a Raspberry
Pi package.

## ✨ Highlights

- 📊 **A conformant OpenMetrics exposition, and every metric name changes.**
  Names follow the grammar (`system.cpu.core 0.idle` →
  `system_cpu_idle_percent{core="0"}`), every family carries `# TYPE`, `# HELP`
  and a `# UNIT` where the value is measured in something, counters are typed
  as counters, string readings come back as `_info` families, values keep their
  full precision and the body ends with `# EOF`. Per-core, per-NIC, per-drive
  and per-process readings become one family with a label, so `sum by (core)`
  has something to group on. The JSON endpoints, the dashboard, Graphite,
  collectd and Python `submit_metrics` report the same keys and values as
  before. `openmetrics format = legacy` reproduces the old body as a migration
  window. (#1533, #1535, #1538, #1539)
- 📥 **New module: `GearmanClient`, a Mod-Gearman worker and result channel.**
  Optional, off by default, and it speaks both flavours — ConSol's Mod-Gearman
  for Naemon and Nagios Enterprises' Nagios-Mod-Gearman for Nagios Core 4.5+.
  `mode = agent` answers for the host it runs on; `mode = proxy` runs a whole
  hostgroup's checks from one box. Windows and Linux. **Experimental and not
  yet tested at scale** — try it on a few hosts first. (#1542)
- 🔒 **A settings source, include or attachment that is not `https://` is
  refused.** The remote store is the agent's whole configuration, re-read at
  boot and on every housekeeping pass, and over plain `http://` nothing
  authenticates the server. Opt back in per host with `allow plaintext = true`
  in `boot.ini`; every plaintext fetch is then logged as `INSECURE`. (#1529)
- 🛡️ **The audit's low-severity tier lands, in three parts.** A request may no
  longer weaken a credentialed target's transport security or re-address
  `submit_smtp` mail; script arguments, `check_docker`'s endpoint and the
  remote-connection checks are confined; and the web server sends browser
  hardening headers, negotiates TLS 1.3 on Linux and stops minting a session
  token per request. (#1550, #1551, #1552)
- 🔑 **`check_tcp` and `check_ssh` verify the server certificate by default.**
  `verify` defaulted to `none`, so a TLS check handshook against any
  certificate at all and reported `ok`. It now defaults to `peer` with `ca=`
  falling back to the agent's own trust bundle, and the checks gained
  certificate identity, SAN and STARTTLS-service keywords. (#1547)
- 🔁 **Agent-to-agent checking works, over the REST API, and the raw protobuf
  web API is gone.** `POST /query.pb` let a caller write the header the core
  reads its identity from; its only consumer was `NSCPClient`, which had never
  actually worked. `check_remote_nscp` and friends now go through
  `/api/v2/queries`, authenticated. (#1552)
- 🧪 **New modules and check commands are marked *experimental*.** A statement
  about stability, not about breakage: `nscp test`, the web UI, the REST API
  and the reference docs all say which checks may still change their options,
  keywords or output. (#1543)
- 🎨 **The prompt and the web UI paint filter expressions.** Both now read the
  check's own vocabulary and colour a `filter=`, `warning=` or `detail-syntax=`
  as you type it — a keyword the check does not offer is red before the check
  is ever run. A new `GET /api/v2/queries/{query}/help` is what the browser
  reads. (#1540, #1541)
- ⏱️ **Reloads wait for the checks that are running.** A settings reload holds
  new checks off a module while it applies the new configuration, a module can
  no longer unload or restart itself from inside a request it is serving, and
  connect and TLS handshake now count against a client's configured timeout.
  (#1531)
- 📦 **A fifth off the Linux install, and much more off Windows.** Code every
  plugin compiled privately moved into shared libraries, and OpenSSL ships as
  DLLs instead of being linked into each of NRPE, NSCA, check_mk, the web
  server and the HTTP clients. (#1544, #1556)
- 🪟 **Windows ARM64 is packaged again, and there is a Raspberry Pi package.**
  `NSCP-<version>-ARM64.msi`/`.zip` are back (without `PythonScript`, and the
  ARM64 MSI does not bundle the VC runtime), and
  `NSCP-<version>-debian-trixie-arm64.deb` covers Raspberry Pi OS 64-bit and
  Debian 13 arm64. (#1546)

## 🔍 Detailed changes

### 📊 OpenMetrics — named, typed, described and labelled

The endpoint used to paste the JSON keys into the exposition verbatim. Names
carried `.`, `%`, spaces and colons (`system_mem_commited.avail`,
`system_cpu_core 0.idle`, `disk_free_C:.total`); there was no `# TYPE` and no
`# EOF`; values were truncated to six significant digits, so 16 GB of memory
scraped as `1.6554e+10`; monotonic counts were typed as gauges, so `rate()`
was unsafe on them; and string readings — uptime, boot time, MAC address,
power source — were dropped entirely. A strict parser rejected the body, and
the scenario page told you to repair the names with `metric_relabel_configs`.

Three things changed, and each of them renames families.

**Names follow the grammar.** `%` becomes the word `percent`, everything else
outside `[a-zA-Z0-9_]` becomes `_`, runs collapse, and a name that would not
start with a letter borrows a `metric_` prefix.

| JSON key                  | Metric name                   |
|---------------------------|-------------------------------|
| `system.mem.physical.%`   | `system_mem_physical_percent` |
| `system.cpu.core 0.idle`  | `system_cpu_core_0_idle`      |
| `disk.free.C:.total`      | `disk_free_C_total`           |

**Every metric carries a description, a type and a unit.** `# HELP` on every
built-in family, `# UNIT` wherever the value is measured in something — which
renames the family again, since a family that declares a unit has to end in it
(`system_mem_physical_total` → `system_mem_physical_total_bytes`). Counters
are typed as counters and carry the reserved `_total` suffix on their sample;
strings come back as an `_info` family in the `node_uname_info` shape.

**Per-instance metrics are one family with a label.**

```text
# TYPE system_cpu_idle_percent gauge
system_cpu_idle_percent{core="0"} 93
system_cpu_idle_percent{core="1"} 91
system_cpu_idle_percent{core="total"} 95
```

The label is `core`, `cpu`, `nic`, `zone`, `battery`, `exe`, `disk`, `drive`
or `pdh_instance` depending on the bundle — `pdh_instance` rather than
`instance`, because Prometheus attaches its own `instance` label to every
sample. Windows and Linux spell a CPU core differently in the JSON key
(`core 0` and `core_0`); neither spelling reaches the label, which is the bare
`0` on both, so one query works across a mixed fleet.

Around that:

- **`/api/v2/metrics?meta=1`** serves the same keys and values with their help
  text, unit, type and labels under a `metadata` object. Without `meta` the
  endpoint is byte for byte what it was.
- **GraphiteClient can send the labels as carbon tags** (`metric tags = true`,
  off by default — a carbon older than 1.1 stores `path;core=0` as the name).
- **CollectdClient mappings can read the labels and the types.** A variable set
  to `label:core` expands to every value of that label instead of a regular
  expression over flat keys, and `auto:` sends whatever the producing module
  declared a counter as a DERIVE and everything else as a GAUGE.
- **Predefined PDH counters can describe themselves** with `help` and `unit`
  keys, and **Python `fetch_metrics` accepts a dict per value**
  (`{"value": 42, "help": "…", "unit": "bytes", "type": "counter"}`, plus
  `"labels"`).
- **Windows only: `system.mem.page.%` and `system.mem.physical.%` report
  different numbers**, because they were reporting the wrong thing — both
  divided the commit charge by the commit limit. Alert thresholds tuned
  against the old reading need re-checking.

### 📥 GearmanClient — Mod-Gearman, either flavour

A Naemon or Nagios Core installation running Mod-Gearman keeps its scheduler,
its check definitions and its escalations; the agent registers for the queues
you name, pulls jobs off `gearmand` and answers them as native NSClient++
queries. Nothing listens on the monitored host.

| Setting | Effect |
|---|---|
| `mode = agent` | Answers only for the host it runs on; a job for another `host_name` is answered UNKNOWN |
| `mode = proxy` | Answers every check on the queues it registered — one Windows box running a whole hostgroup through `check_nrpe`, `check_wmi` and the rest |

The same module submits passive results into the core's result queue
(`/settings/gearman/client`, channel `GEARMAN`, command `submit_gearman`),
which is what lets a Mod-Gearman installation drop NSCA. The two halves are
independent.

Two things to unlearn when writing the `check_command` on the core, since
neither fails in a way that names the cause: write `host=$HOSTADDRESS$`, not
`-H $HOSTADDRESS$` (a two-character first token puts the argument parser into
key-value mode and the check answers with a help screen), and
`warning=load gt 80`, not `warning=load>80` (`>` is a metacharacter, and
`allow nasty characters` is `false` by default). See
[Mod-Gearman](https://nsclient.org/docs/scenarios/mod-gearman/) for the full
setup on either core.

The module is marked **experimental**, and that mark is doing real work here:
its settings, queue handling and output may still change, and while it has been
run end to end against a real `gearmand` on both cores, it has **not been tested
at scale** — not against hundreds of hosts, a deep job backlog, or a proxy
answering for a large hostgroup. Roll it out to a slice of the estate first and
keep the existing transport until you are satisfied. Reports of how it behaves
on a real workload are exactly what the experimental mark is asking for.
(#1542)

### 🛡️ Security

The low-severity tier of the audit landed in three parts, alongside a second
undefined-behaviour sweep and the settings/web/build hardening from #1529.

**Outbound clients.** The request-override guard now covers the keys that
decide *how* a connection is protected — `verify`, `insecure`, `no-psk`,
`ssl`, `tls-version`, `ca`, `certificate`, `allowed-ciphers`, `dh` — and, for
SMTP, `recipient` and `sender` (behind their own `allow recipient override`).
`proxy=` and `no-proxy=` count as moving the request, since a caller-chosen
proxy receives it whole with the configured NRDP token in it.
`payload-length` is clamped to what each protocol accepts, 65536 for NSCA and
1 MiB for NRPE. (#1526, #1550)

**Scripts and check targets.** A NUL in a script argument is refused —
`CreateProcessW` reads the command line as a C string, so it truncated there
and silently dropped every operator-fixed argument after the substitution
point. `ext-scr add --import` reads only from the script folders. A script now
receives only its own stdin and its own stdout/stderr pipe ends instead of
every inheritable handle of the service. `host=` on a docker check must match
the configured `endpoint`. And on Linux, a script section with `user`,
`domain` or `password` set is refused rather than run as the service account:
those keys are implemented by the Windows launcher only, so a script sandboxed
with `user = nobody` was not sandboxed at all. (#1523, #1551)

**The web server.** Every response carries `X-Frame-Options: DENY`,
`X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer` and a content
security policy, plus `Strict-Transport-Security` over TLS — so a page that
embeds the agent's UI in a frame will stop working, which is the point.
`[/settings/WEB/server]` gains `tls version` (default `1.2+`) and
`allowed ciphers`. Logging out calls `DELETE /api/v2/login`, so the bearer
token stops working immediately; the in-memory log buffer is capped at 1000
entries, where an unauthenticated peer could previously add one per rejected
request for the life of the process; and `nscp web install-ui` no longer stages
its download in `${temp}`. (#1552)

**Elsewhere.** The shared `/settings/default/password` is registered sensitive
by the core rather than by whichever server module happens to be loaded, so
every agent redacts it. Elastic and Op5 submissions log when credentials go
over an unverified `https` link, as the Icinga, NRDP and NRPE clients already
did — and the Icinga warning, which repeated on every submission, is logged
once per target now. `allowed hosts` finally understands the `*` ranges it has
always advertised (`192.168.1.*`, `10.*`, a bare `*`); such an entry used to
throw out of the address parser and take the whole listener with it. The
Windows release build pins every third-party action to a commit and verifies
every download against `.github/dependency-checksums.txt`. (#1529, #1532,
#1534, #1537)

**Fleet bundle signatures changed shape, and this one needs action.** An
Ed25519 signature used to cover the bare SHA-256 digest of a bundle's bytes,
which bound nothing about *which* bundle those bytes were: an old signed blob
could be re-advertised under a new id, name or version and still verify. It now
covers a canonical descriptor of the bundle's identity, which means the fleet
server must be upgraded before — or at the same time as — the agents. A
mismatch is safe but inert: the agent logs `signature verification failed`,
keeps the configuration it last applied, and stops picking up changes. (#1536)

### 🔁 Agent-to-agent checks over REST

`POST /query.pb` and `POST /settings/query.pb` are removed. The first handed
the core a message whose header the caller wrote, and the core reads the
calling module and user out of that header. The second had been unreachable for
several releases. Nothing that talks to an agent over HTTP used them: Icinga's
`check_nscp_api` asks for `GET /query/{name}`, untouched, and the web UI uses
`/api/v2`.

Their only consumer was NSClient++ itself, through `NSCPClient` — and that
never worked: it passed the serialized message as the HTTP request target, so
every request was malformed, and the configured password was never sent.
`check_remote_nscp`, `remote_nscp_query` and `remote_nscpforward` now run the
command through `GET /api/v2/queries/{command}/commands/execute`. If you have
an `NSCP` target configured:

| Setting | Was | Now |
|---|---|---|
| `path` | `/query.pb` | `/api/v2/queries` |
| TLS | off unless `ssl = true` | **on** unless `no ssl = true` |
| `password` | read, never sent | sent; the remote's `admin` user needs `queries.execute` |

`exec_remote_nscp` and `submit_remote_nscp` are removed rather than ported:
both posted an NRPE-style string to the protobuf route, which the remote parsed
as an empty message and answered with nothing — and the submit path reported
success regardless. Use NSCA, NRDP or another submit client for passive
results. (#1552)

### 🧪 Experimental modules and commands

A module or check command that is new enough that its options, filter keywords
and output may still change now says so: `nscp test` appends `(experimental)`
in `queries`, `aliases`, `list` and `plugins` and shows a `Status:` line in
`desc`, the web UI shows a chip, the REST API reports an `experimental` field,
and the reference documentation renders a marker in the command tables and a
note on the command. The recently added `check_*` commands of `CheckDisk`,
`CheckDocker`, `CheckNet`, `CheckNSCP` and `Scheduler` are marked, as are the
`CheckMSSQL`, `CheckMySQL`, `CheckSecurity`, `CheckWindowsApps`,
`GearmanClient` and `NSCANgClient` modules in full. Out-of-tree modules declare
it in `module.json`. (#1543)

### 🎨 Filter expressions, painted

The prompt already knew a command name from a typo. It did not know anything
about what came after the `=`, which is where the mistakes actually are:
`filter=fre < 10%` is a check that runs, matches nothing and reports OK. The
value of every option that takes a filter expression or a syntax template is
now read as what it is, following the where grammar and the placeholder rules
the engine itself uses — a keyword the check offers is painted, one it does not
is red, before enter is pressed. Filter functions, operators and number+unit
literals each get their own colour.

The web UI's arguments field does the same, from the same registry data:
`GET /api/v2/queries/{query}/help` returns one check's whole vocabulary — every
option with its default, flags and description, and every filter keyword it
offers. An alias declares no keywords of its own, so the endpoint follows it to
the command it stands for and says which one in `keyword_source`. (#1540,
#1541)

### ⏱️ Threading, reloads and timeouts

The ten highest-severity findings of the concurrency audit are fixed, and
several of them are visible from outside:

- A settings reload holds new checks off a module while its `loadModuleEx`
  applies the new configuration, and waits up to five seconds for checks
  already inside it to return. A reload is no longer instantaneous on a busy
  agent; if a check holds a module longer than that, the reload proceeds anyway
  and logs which module it was.
- Unloading the module that is serving the request is refused instead of taking
  the agent down with it — in practice
  `POST /api/v2/modules/WEBServer/commands/unload`. Reloading a listener from
  inside a check that the same listener is serving is refused too, instead of
  leaving that listener dead.
- Configuration downloaded over HTTP gives up on a read or write that stalls
  for 30 seconds, instead of waiting indefinitely, and no longer holds the
  settings instance lock while it downloads.
- Submissions over NRPE, NSCA, NSCP and check_mk apply the configured timeout
  to connecting and to the TLS handshake, not just to the exchange.

Underneath: the Lua script manager and the collector pointers are published
atomically so a reload cannot free them under a running check, the scheduler
watchdog no longer re-arms the pool during shutdown, a socket server refuses to
be stopped from one of its own threads, the Python function registry is read
under the GIL, and a `CheckEventLog` filter object no longer closes a handle it
does not own. (#1531, #1534)

### 🐛 Bug fixes

- **`check_nt` `FILEAGE` checks one file instead of a directory of them.** It
  mapped onto `check_files`, which walks a whole tree, so a directory argument
  reported whichever file the walk happened to emit first — not the oldest, not
  the newest, just arbitrary. It maps onto `check_single_file` now; a directory
  fails with an error.
- **The Windows installer no longer rewrites NRPE transport security it did not
  configure.** The MSI recognised only `insecure = true` and
  `verify mode = peer-cert`, so a listener running TLS without client
  certificates, or one with a hand-written cipher string, fell through and got
  a preset applied over it. (#1562)
- **`nscp nrpe install` writes `use ssl`**, not `ssl = true` — a key the server
  never reads. On a host where `use ssl = false` had been set previously, the
  command claimed encryption and client-certificate authentication while the
  listener stayed in plaintext. The legacy cipher default also drops its
  `!ADH`, which never excluded the anonymous elliptic-curve suites.
- **The PDH counter browser narrows on every filter and ignores case.**
  `--list`, `--filter` and `--counter` shared one variable, so whichever came
  last won and the others were silently discarded; `--filter` is repeatable
  now. Matching is case insensitive, so `--list disk` finds what `--list Disk`
  finds.
- **A round-robin counter with a zero or unparseable buffer size is refused**
  and named in the log, instead of being loaded with a buffer that holds
  nothing.
- **A collectd value list naming a metric the snapshot does not carry is no
  longer sent as a zero** — it reported a measurement nobody took. Such a value
  list is skipped in whole, since a collectd value list is positional.
- **`check_ping` keeps listening for its own echo reply** instead of giving up
  on the first reply that arrives, an HTTP status line with a reason phrase
  parses, every line of a remote check result is kept, and a string Python
  cannot encode no longer crashes the agent.
- **`check_dns`'s `host=` description** said the wrong thing. (#1545)

### 📦 Packaging

- **Shared runtime libraries.** `nscp_net.dll` (sockets and TLS),
  `nscp_client.dll` (the sender modules' shared command line), `nscp_json.dll`
  and OpenSSL as `libcrypto-3-x64.dll` / `libssl-3-x64.dll` now ship next to
  `nscp.exe`, one copy for the whole service, where before NRPE, NSCA,
  check_mk, the web server, the HTTP clients and the checksum checks each
  carried their own. `plugin_api.dll` absorbed the settings and program-options
  helpers. About a fifth off the install on Debian and RedHat, and more than
  that on Windows. The legacy XP build still links everything statically.
  (#1544, #1556)
- **Windows ARM64 is back** as `NSCP-<version>-ARM64.msi` and `.zip`. Two
  differences from x64: no `PythonScript` (the package is cross-compiled and
  there is no ARM64 CPython to embed), and the MSI does not bundle the Visual
  C++ runtime, because Microsoft ships no ARM64 merge module for this toolset —
  install
  [vc_redist.arm64.exe](https://aka.ms/vs/17/release/vc_redist.arm64.exe)
  first on a fresh machine. (#1546)
- **A Raspberry Pi OS package**, `NSCP-<version>-debian-trixie-arm64.deb`,
  built on Debian 13 for Raspberry Pi 3 and newer and for Debian 13 arm64 in
  general. 64-bit only, and without the managed (C#) plugin API, since Debian
  does not package the .NET SDK. (#1546)
- **The web bundle is built with `npm ci` and gated on `npm audit`**, so the
  bytes in the web zip and in the MSI's `web/dist` match `package-lock.json`.
  Pull requests build only the newest RedHat, and a failed dependency download
  fails at the download instead of somewhere later.

## ⚠️ Upgrade notes

- **Every OpenMetrics family name changes.** Drop any `metric_relabel_configs`
  block that rewrote dots to underscores — the agent does that itself now.
  Update dashboards, recording rules and alerts: `system_cpu_core 0.idle` is
  `system_cpu_idle_percent{core="0"}`, `disk_free_C:.total` is
  `disk_free_total_bytes{drive="C:"}`, `workers_jobs` is `workers_jobs_total`.
  Exclude `core="total"` from anything that aggregates over cores. If
  dashboards cannot be updated first, set `openmetrics format = legacy` under
  `[/settings/WEB/server]` as a migration window — it is deprecated and will be
  removed.
- **Upgrade the fleet server before or with the agents.** Bundle signatures now
  cover the bundle's identity, not only its bytes. A version mismatch is inert
  rather than damaging: the agent keeps the configuration it last applied and
  stops picking up changes.
- **A settings source, include or attachment over plain `http://` is refused.**
  Move it to `https://`, or set `allow plaintext = true` under `[tls]` in
  `boot.ini` per host.
- **`check_tcp` / `check_ssh` against an internal or self-signed service now
  fail** with `tls_handshake_failed`. Point `ca=` at the issuing CA or add
  `verify=none`. `sni=` on a non-TLS connection is now rejected rather than
  ignored.
- **`POST /query.pb` is gone.** If you have an `NSCP` client target, remove an
  explicit `path` or point it at `/api/v2/queries`, expect TLS unless you set
  `no ssl = true`, and give the remote's `admin` user the `queries.execute`
  grant. `exec_remote_nscp` and `submit_remote_nscp` are removed.
- **Requests may no longer weaken a credentialed target's transport security**
  (`verify`, `insecure`, `ssl`, `ca`, `tls-version`, `proxy`, …) or re-address
  `submit_smtp` mail. Supply the credentials with the request, configure the
  variant as its own target, or set `allow host override = true` /
  `allow recipient override = true`.
- **External scripts with `user`, `domain` or `password` set are refused on
  Linux** — those keys were never implemented there. Put the identity change in
  the command itself with `sudo`.
- **The web UI cannot be framed** any more, and `check_nt FILEAGE` naming a
  directory now fails instead of reporting an arbitrary file's age.
- **A hand-rolled deployment must copy the new shared libraries** from the
  installation root alongside `modules\*.dll`, the OpenSSL DLLs included.
  Installing from the MSI or the Debian/RedHat packages needs nothing.
- **On Windows ARM64**, install the VC++ ARM64 redistributable before the agent
  on a fresh machine, and use the x64 package under emulation if you need
  `PythonScript`.

Security notices for this release are on the
[security notices page](https://nsclient.org/docs/security/notices/), and the
full list of behaviour changes is on the
[upgrading page](https://nsclient.org/docs/setup/upgrading/).

## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.22.0){ .md-button }

// Michael Medin

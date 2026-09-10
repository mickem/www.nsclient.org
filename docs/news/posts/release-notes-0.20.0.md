---
date:
  created: 2026-09-10
---

# 0.20.0 .NET plugins return, the WEB server keeps passive results, and a security review of NRPE and TLS

0.20.0 brings back the `DotnetPlugins` module — now hosting an installed .NET
runtime through `hostfxr`, so it works on Linux as well as Windows — and
teaches the WEB server to keep passive check results in memory and serve them
over REST, so a monitoring server that cannot be pushed to can poll a host's
scheduled checks out of the agent in one request. A review of the NRPE path and
the shared TLS layer closed a handful of findings, the most important being
that generated TLS private keys were world-readable and that a generated CA
shipped its private key inside the `ca.pem` handed to clients.

Alongside that, the undefined-behaviour audit that followed #1499 fixed roughly
seventy crash and memory-safety findings across the tree, the client
host-override guard from 0.19.0 closes two ways past it, stopping the service
no longer waits minutes on a stalled Windows Update search, every enumerating
check is now tested against an empty filter result, and the tree builds with
GCC 16.

## ✨ Highlights

- 🔌 **.NET plugins are back, on Windows and Linux.** `DotnetPlugins` is built
  again, hosting an installed .NET runtime (8.0 or newer) through `hostfxr`
  instead of the old Windows-only C++/CLI build. Nothing is bundled and the
  module is not loaded unless you enable it; the Windows installer regained
  its ".NET plugin support" feature. Plugins written against the old .NET
  Framework `NSCP.Core.dll` need a rebuild against the `net8.0` one — the
  interfaces are unchanged. (#1481)
- 📤 **The WEB server can cache passive results and serve them over REST.**
  Enable `[/settings/WEB/server/results]` and `WEBServer` registers a
  submission channel, keeps one result per key (newest or worst, your choice)
  and answers `GET /api/v2/results`. The bundled `check_nsclient` moves to
  1.1.0, whose `results feed` polls that cache and hands everything in it to
  Nagios as passive results — one active check per host instead of one per
  service. A new scenario walks through the Nagios Core setup. (#1498)
- 🔒 **NRPE and the shared TLS layer reviewed.** Generated private keys are
  now `0600` and a generated CA keeps its key out of `ca.pem`; the inbound TLS
  handshake is bounded by the listener's `timeout`; the NRPE client says so
  when it is not authenticating the server; a short v3/v4 packet can no longer
  smuggle unchecksummed trailing bytes into the command; and the Logjam-broken
  512-bit DH parameter file is gone. (#1496)
- 🛡️ **Undefined-behaviour audit.** Roughly seventy findings fixed, one commit
  each. Three were reachable from outside the agent: a malformed chunked HTTP
  response could hang it, an empty `POST /console/exec` command could crash
  it, and `filter_perf sort=normal` could crash on the Nagios `U` marker. The
  rest were memory errors on common Windows checks, races on module reload and
  unload, and unguarded threshold arithmetic. (#1505)
- 🔐 **Two ways past the client host-override guard are closed.** A secret
  carried inside the target's `address` (`?token=`, `user:password@`) now
  counts as the configured credential it is, and a target with a credential
  but no address no longer adopts the caller's `host=` as its own.
- ⏱️ **Stopping the service no longer waits on stalled collectors.** The
  Windows Update search and the WMI perf-data queries that CheckSystem and
  CheckDisk issue at start are abandoned on shutdown instead of holding the
  unload for minutes. (#1504, #1507)
- 🧪 **Every enumerating check is tested against an empty filter result.** The
  path that killed the agent in 0.18 (#1499) now has one integration case per
  check, so a regression fails a test instead of the process. (#1503)
- 🐧 **Builds with GCC 16**, which defaults to C++20; the C++ standard is now
  declared instead of taken from the compiler. (#1479, #1483)

## 🔍 Detailed changes

### 🔌 DotnetPlugins — hosted through hostfxr on Windows and Linux

The old module was a C++/CLI build that only ever worked on Windows and was
dropped from the build years ago. The new one is native code that locates an
installed .NET runtime (`DOTNET_ROOT`, the registered install location, or the
platform's default install folders — or `runtime path` if you want to pin it),
loads `hostfxr`, and hosts the managed plugin API `NSCP.Core.dll` from
`modules/dotnet/`. Plugins are declared under `[/settings/dotnet/plugins]`:

```ini
[/modules]
DotnetPlugins = enabled

[/settings/dotnet/plugins]
MyPlugin = MyPlugin.dll
```

Every handler the module advertises is wired: commands, submission channels,
command-line exec and log messages all reach the managed side. Only a
`hostfxr` built for the process' architecture is accepted, and the
native/managed boundary pins its calling convention on both platforms. The
Windows installer's ".NET plugin support" feature installs the module and the
managed API; the Linux packages ship the same files when built with the dotnet
SDK, and a C# sample plugin is built (never shipped) to keep the API honest.
See [Extending with .NET](https://nsclient.org/docs/extending/dotnet/) and the
[DotnetPlugins reference](https://nsclient.org/docs/reference/generic/DotnetPlugins/).

### 📤 WEBServer — a passive result cache served over REST

The usual passive flow pushes results from the agent to the monitoring server.
That fails when the server has no NSCA/NRDP receiver or the agent has no route
in. The WEB server can now invert it: with the cache enabled it registers a
submission channel (`WEB` by default), keeps whatever is submitted to it —
scheduled checks from `Scheduler`, `check_and_forward` from `CheckHelpers`,
anything that submits to a channel — and serves it back on request.

| Setting (`/settings/WEB/server/results`) | Default | Meaning |
|---|---|---|
| `enabled` | `false` | Register the channel and serve the endpoints; read at web server start |
| `channel` | `WEB` | The submission channel to listen on |
| `primary index` | `${host}/${alias-or-command}` | The key one result is kept under |
| `mode` | `last` | `last`: newest result per key wins; `worst`: the most severe since the last poll wins |
| `clear on poll` | `true` | `GET /api/v2/results` drains what it returns |
| `max entries` | `1000` | Keys kept before the oldest is evicted |
| `max age` | none | Results older than this are dropped |

Four endpoints expose the cache — `GET /api/v2/results`,
`GET /api/v2/results/{key}`, `DELETE /api/v2/results` and
`DELETE /api/v2/results/{key}` — behind the new `results.list`, `results.get`
and `results.delete` privileges, which only the `full` role carries:

```
nscp web add-role --role poller --grant results.list,results.get,login.get
```

The cache survives a settings reload with its contents, while `enabled` and
`channel` only take effect on a restart because a channel cannot be registered
from a reload. The bundled `check_nsclient` (Windows MSI and Linux packages
alike) moves from 1.0.1 to 1.1.0, which adds `results list`, `results show`,
`results delete`, `results clear` and `results feed`; the last polls an agent's
cache and submits every entry to Nagios as a passive check result. The
[REST results page](https://nsclient.org/docs/api/rest/results/) has the
contract and the
[Polled Passive Checks (Nagios Core)](https://nsclient.org/docs/scenarios/nagios-result-cache/)
scenario the end-to-end setup.

### 🔒 NRPE and the shared TLS layer — review findings

A review of the wire codec, the server parser and protocol, both NRPE modules
and the socket/TLS layer beneath them. None of it is remotely exploitable for
code execution past `allowed hosts`.

- **Generated TLS private keys were world-readable.** `write_certs` used a
  plain `fopen`, so the unencrypted key a default NRPE start generates landed
  at `0644`. The CA branch also wrote the CA private key into the `ca.pem`
  operators are told to distribute, letting any recipient mint certificates
  that pass `verify mode = peer-cert`. Keys are now `0600` (a restricted DACL
  on Windows) and a generated CA keeps its key in `ca-key.pem`.
- **The inbound TLS handshake had no deadline.** The connection timer was armed
  only after the handshake, so a permitted host could open sockets, send
  nothing and pin connections indefinitely. It is now armed first, bounded by
  the listener's `timeout`.
- **The NRPE client never authenticated the server.** `verify mode` defaults to
  `none`; the default stands, but the client now logs one error per target at
  its first check, and generated certificates carry a usable SAN so
  verification is possible at all.
- **A short v3/v4 packet let unchecksummed bytes into the command.** The
  decoder bounded the payload by the bytes received rather than the declared
  length the CRC covers.
- **The 512-bit DH parameter file is no longer shipped.** Unused by default but
  Logjam-broken, and inherited by anyone who copied the shipped default into
  `dh`.
- Smaller fixes: the peer certificate CN is constrained before it becomes a
  policy principal, `workarounds`/`single` no longer leak into the TLS verify
  mask, every documented `tls version` spelling is accepted (`tlsv1.3+`,
  `1.0+`, `sslv3+`, `any`, … were rejected with "Invalid tls version", which an
  NRPE listener reported as "listener failed to start"), and a set of NRPE
  codec bugs — wire version 4 unrecognised, packets declared complete early,
  length underflows, a re-sending response loop.

### 🔐 Client modules — two ways past the host-override guard

The 0.19.0 guard refuses a request that moves a credentialed target's
destination, but it only recognised a credential in a `password` or `token`
key. A secret inside the address — `?token=SECRET` in the URL, or
`user:password@host` — looked like no credential at all, so `host=` could
redirect it. And a target that supplied a credential but named no address had
the caller's `host=` recorded as its own, so the guard compared the host with
itself. A credential now counts wherever it is written and a target records
only an address it names. The remedies are unchanged: pass the credential with
the request, configure each destination as its own target, or set
`allow host override = true`.

### 🛡️ Undefined-behaviour audit — crash and memory-safety fixes across the agent

After #1499 the C++ tree was scanned for the same class of bug and roughly
seventy findings were fixed, one commit per finding (#1505). Beyond the three
externally reachable ones in the highlights, the bulk were memory errors on the
default paths of common Windows checks (event log records, WMI arrays, task
scheduler COM objects, process snapshots, `check_cpu` and `check_pagefile`
temporaries), races when a module is reloaded or unloaded (a module unload now
waits for its in-flight dispatches, a plugin is never unloaded mid-call,
reloads no longer rewrite server and client tables under live workers), and
unguarded arithmetic in thresholds and unit suffixes. A few inputs that used to
misbehave are now rejected instead:

| Input | Now |
|---|---|
| `check_cpu time=0` | Error: the window must be at least one second |
| A threshold or unit suffix that overflows 64 bits (`used > 1.0e30T`, `time=5000000w`) | Reported as an error instead of wrapping |
| A module whose load fails | Dropped from the plugin list; no longer answers `exec` |
| `NSClientServer` / `CheckMKServer` on a settings reload | Restart their listener, as `NRPEServer` already did; open connections are dropped |
| A Python script unloading `PythonScript` | Refused |

### ⏱️ CheckSystem and CheckDisk — shutdown no longer waits on stalled collectors

Stopping the service shortly after start could take minutes (#1504). The whole
delay sat in the CheckSystem unload: its collector thread was blocked in the
synchronous Windows Update search the OS updates collector issues on its first
cycle, which goes online to Windows Update or WSUS and routinely takes minutes
on a server. The search now runs asynchronously and is aborted on shutdown,
the module stays mapped until the abandoned search has let go of it, and the
WMI perf-data queries CheckSystem (network, temperature, CPU frequency,
battery) and CheckDisk (disk I/O) issue — which stall while `WmiApSrv`
restarts — are abandoned the same way. (#1507)

### 🐧 Build and CI

- GCC 16 (Debian unstable) failed on two fronts, neither a regression: under
  its default `gnu++20` the generated plugin instance no longer
  aggregate-initialised, and the standalone `check_nscp` clients lacked the
  plugin singleton their inline logging members reference. Both fixed, and the
  C++ standard is now declared in CMake instead of taken from the compiler
  (#1479, #1483). The vendored simpleini header builds under C++17 (#1509).
- CI cancels superseded runs per ref and runs the sanitizer jobs on `main`
  only, so a pushed fix or a run of merges no longer queues full builds nobody
  will release (#1510).

### 🧪 Testing

One integration case per enumerating check passes a filter that matches
nothing and asserts the documented empty contract: `check_process`,
`check_network`, `check_registry_key`, `check_registry_value`,
`check_printqueue`, `check_printjobs`, `check_drivesize`, `check_disk_io`,
`check_disk_health`, `check_files`, `check_share`, `check_tasksched`,
`check_connections` and `check_logfile` with a `column()` threshold (#1503).

### 📚 Documentation

- New scenario: [Polled Passive Checks (Nagios Core)](https://nsclient.org/docs/scenarios/nagios-result-cache/).
- New REST page: [Results](https://nsclient.org/docs/api/rest/results/).
- New extending page: [.NET plugins](https://nsclient.org/docs/extending/dotnet/), and the
  `DotnetPlugins` reference is filed under the generic modules now that it runs on both platforms.
- The WEB server reference documents the `/settings/WEB/server/results` section.

## ⚠️ Upgrade notes

- 🔒 **Generated TLS private keys are now created `0600`, and a generated CA
  keeps its key out of `ca.pem`.** Existing files are not touched: run
  `chmod 600 /etc/nscp/security/certificate.pem`, and if you distributed a
  generated `ca.pem`, regenerate that CA and re-issue client certificates —
  anyone holding the old file can mint certificates that pass
  `verify mode = peer-cert`.
- 🔒 **The client host-override guard also covers a credential kept inside the
  target's address.** Nothing to do unless you relied on `host=` to point a
  credentialed target at several hosts; use `target=`, pass the credential
  with the request, or set `allow host override = true`.
- 🔒 **Undefined-behaviour audit: some inputs are now rejected.** See the table
  above; nothing to do unless you relied on one of them.
- 🔒 **Inbound TLS handshakes are bounded by the listener's `timeout`.** A
  client on a link too slow to complete a handshake within `timeout` (30 s by
  default) is dropped; raise `timeout` on the listener if that is too tight.
- 🔒 **The NRPE client logs one error per target when `verify mode = none`.**
  The default is unchanged; set `verify mode = peer-cert` with `ca` pointing at
  the issuer to silence it and actually authenticate the server. Regenerate an
  existing generated certificate to get a usable SAN.
- 🔒 **`security/nrpe_dh_512.pem` is no longer shipped.** If you set `dh` to it
  explicitly, change it to `${nrpe-dh}/nrpe_dh_2048.pem` before upgrading or
  the listener will fail to start. An existing copy on disk is left alone.
- 🔌 **`DotnetPlugins` is back.** Not loaded unless you add
  `DotnetPlugins = enabled` to `[/modules]`; no runtime is bundled (8.0 or
  newer must be installed). Plugins built against the pre-0.6 .NET Framework
  `NSCP.Core.dll` must be rebuilt against the `net8.0` one.
- 📤 **The WEB passive result cache is off by default.** Enabling it needs a
  restart, and `results.list`/`results.get`/`results.delete` must be granted
  to whoever polls. The bundled `check_nsclient` is now 1.1.0; no existing
  invocation changes.
- 🔧 **`tls version` accepts every spelling it documents.** Nothing to do; the
  default `tlsv1.2+` was never affected.

Full detail on the security items lives in [Security notices](https://nsclient.org/docs/security/notices/); the operator
actions are mirrored on [Upgrading](https://nsclient.org/docs/setup/upgrading/).


## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.20.0){ .md-button }

// Michael Medin

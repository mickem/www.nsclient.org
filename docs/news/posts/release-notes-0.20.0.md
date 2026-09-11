---
date:
  created: 2026-09-10
---

# 0.20.0 .NET plugins return, the WEB server keeps passive results, and more security fixes

0.20.0 brings back .NET plugins — on Linux as well as Windows this time — and
lets the WEB server hold on to passive check results so a monitoring server
can collect a host's scheduled checks in a single request instead of being
pushed to. A security review of NRPE and the TLS layer underneath it fixed a
handful of findings; the one to act on is that TLS certificates the agent
generated itself were readable by every local user, and a generated CA handed
its private key to every client it was distributed to.

The release also fixes some seventy crash and hang bugs found by scanning the
whole code base after the `check_service` crash in 0.19.0, closes two gaps in
the credential guard introduced in 0.19.0, and makes stopping the service
prompt again on Windows hosts where it could hang for minutes.

## ✨ Highlights

- 🔌 **.NET plugins are back, on Windows and Linux.** The `DotnetPlugins`
  module hosts an installed .NET runtime (8.0 or newer), so plugins written in
  C# or F# load on both platforms. Nothing changes on a default install: the
  module stays off until you enable it, and no runtime is bundled. Plugins
  built for the old .NET Framework API need a rebuild against the new
  `NSCP.Core.dll`; the interfaces are the same. (#1481)
- 📤 **The WEB server can keep passive results and serve them over REST.**
  Turn the result cache on and everything submitted to its channel — typically
  scheduled checks — waits in the agent until something polls
  `GET /api/v2/results`. The bundled `check_nsclient` 1.1.0 adds
  `results feed`, which collects that cache and hands every entry to Nagios as
  a passive result: one active check per host instead of one per service, and
  no NSCA or NRDP receiver needed. A new scenario walks through the Nagios
  Core setup. (#1498)
- 🔒 **Generated TLS keys are private now; check yours.** Certificates the
  agent generated itself — including the one a default NRPE start creates —
  were written world-readable, and a generated CA wrote its private key into
  the `ca.pem` meant for clients. New files are created correctly; existing
  ones are left alone, so see the upgrade notes. (#1496)
- 🛡️ **NRPE and TLS hardened.** A TLS handshake can no longer be left open
  forever by a permitted host, a short NRPE packet can no longer smuggle
  unverified bytes into the command, the NRPE client tells you when it is not
  authenticating the server, and the Logjam-broken 512-bit DH parameter file
  is gone. (#1496)
- 🐛 **Seventy crash and hang fixes across the agent.** Three could be
  triggered from outside: a malformed HTTP response from any server the agent
  talks to could hang it, an empty console command over REST could crash it,
  and `filter_perf sort=normal` could crash on the Nagios `U` marker. The rest
  were bugs on the default paths of common Windows checks, races when a module
  is reloaded or unloaded, and thresholds that silently overflowed. (#1505)
- 🔐 **Two ways past the credential guard closed.** A token or password
  written inside a target's `address` is now protected the same way as one in
  its own key, and a target without an address no longer adopts the caller's
  host as its own.
- ⏱️ **Stopping the service is prompt again.** On Windows, stopping shortly
  after start could take minutes while the Windows Update check or a WMI query
  finished; those are now abandoned on shutdown. (#1504)
- 🐧 **Builds with GCC 16** for anyone building from source on a current
  Debian or Fedora. (#1479)

## 🔍 Detailed changes

### 🔌 DotnetPlugins — .NET plugins on Windows and Linux

The old module only ever worked on Windows and had been out of the build for
years. The new one finds an installed .NET runtime — `DOTNET_ROOT`, the
registered install location or the platform's default folders, or a path you
give in `runtime path` — and hosts your plugins through it. Everything a
plugin could do before still works: commands, submission channels,
command-line exec and log messages all reach the managed side.

```ini
[/modules]
DotnetPlugins = enabled

[/settings/dotnet/plugins]
MyPlugin = MyPlugin.dll
```

Assemblies are looked up in `plugin path` (`modules/dotnet` by default,
where `NSCP.Core.dll` lives too). On Windows the installer has a ".NET plugin
support" feature again, selected by default; the Linux packages ship the same
files. See [Extending with .NET](https://nsclient.org/docs/extending/dotnet/)
and the
[DotnetPlugins reference](https://nsclient.org/docs/reference/generic/DotnetPlugins/).

### 📤 WEBServer — a passive result cache served over REST

Passive monitoring normally means the agent pushes results to the monitoring
server. That does not work when the server has no NSCA or NRDP receiver, or
when the agent cannot reach it. The WEB server can now turn it around: with
the cache enabled it listens on a submission channel (`WEB` by default),
keeps whatever arrives there — scheduled checks from `Scheduler`,
`check_and_forward` from `CheckHelpers`, anything that submits to a channel —
and hands it over when polled.

| Setting (`/settings/WEB/server/results`) | Default | Meaning |
|---|---|---|
| `enabled` | `false` | Turn the cache on (takes effect on restart) |
| `channel` | `WEB` | The submission channel to listen on |
| `primary index` | `${host}/${alias-or-command}` | What makes two results "the same check" |
| `mode` | `last` | Which of two results for a check to keep: the newest (`last`) or the most severe (`worst`) |
| `clear on poll` | `true` | Polling empties the cache, so `worst` means "worst since the last poll" |
| `max entries` | `1000` | How many checks to keep before the oldest is dropped |
| `max age` | none | Drop results older than this |

The cache is exposed as `GET /api/v2/results`, `GET /api/v2/results/{key}`,
`DELETE /api/v2/results` and `DELETE /api/v2/results/{key}`. They need the
new `results.list`, `results.get` and `results.delete` privileges, which only
the `full` role has, so grant them to the account that polls:

```
nscp web add-role --role poller --grant results.list,results.get,login.get
```

`check_nsclient` 1.1.0, bundled with the Windows and Linux packages, adds the
`results list`, `results show`, `results delete`, `results clear` and
`results feed` commands; `feed` is the one to schedule from Nagios. The
[REST results page](https://nsclient.org/docs/api/rest/results/) describes
the API and the
[Polled Passive Checks (Nagios Core)](https://nsclient.org/docs/scenarios/nagios-result-cache/)
scenario the complete setup.

### 🔒 NRPE and TLS — what the review found

None of the findings lets anyone past `allowed hosts` run code on the agent.

- **Generated private keys were readable by every local user**, and a
  generated CA put its private key into the `ca.pem` you distribute to
  clients — anyone holding that file could mint certificates the server
  accepts with `verify mode = peer-cert`. New keys are created readable only
  by the agent, and a generated CA keeps its key in a separate `ca-key.pem`.
- **A TLS handshake could be left open forever.** A permitted host could open
  connections, send nothing, and hold them indefinitely. The listener's
  `timeout` now covers the handshake as well.
- **The NRPE client did not authenticate the server.** With `ssl = true` and
  the default `verify mode = none` the link is encrypted but anyone on the
  path could impersonate the server. The default stays, but the client now
  logs one error per target so the choice is visible, and generated
  certificates name the machine rather than only `localhost` so verification
  can actually be turned on.
- **A short NRPE v3/v4 packet could carry extra bytes into the command** that
  the checksum never covered.
- **The 512-bit DH parameter file is no longer shipped.** Nothing used it by
  default, but anyone who copied it into `dh` was running a Logjam-broken
  key exchange.
- Smaller fixes: `tls version` accepts every spelling the documentation lists
  (`tlsv1.3+`, `1.0+`, `sslv3+`, `any`, … used to fail with "Invalid tls
  version", which for an NRPE listener showed up as "listener failed to
  start"), and several NRPE wire-format bugs are fixed, including version 4
  packets not being recognised by the server.

### 🔐 Client modules — the credential guard covers the address too

0.19.0 stopped a caller from redirecting a target that carries a credential
to a host of their choosing. It missed two cases: a secret written inside the
address itself (`?token=SECRET` in the URL, or `user:password@host`), and a
target that had a credential but no address, which took the caller's host as
its own. Both are closed. If you relied on either, the options are the same as
in 0.19.0: pass the credential with the request, configure one target per
destination and pick it with `target=`, or set `allow host override = true`.

### 🛡️ Crash and hang fixes across the agent

After the `check_service` crash in 0.19.0 (#1499) the whole code base was
checked for the same kind of mistake, and roughly seventy were fixed. Most
were on paths ordinary checks take every day: reading event log records, WMI
results and scheduled tasks, taking process snapshots, `check_cpu` and
`check_pagefile`. Others showed up when a module was reloaded or unloaded
while a check was running, or when a threshold or unit suffix was larger than
the agent could represent. As a side effect, a few inputs that used to do
something odd are now rejected outright:

| Input | Now |
|---|---|
| `check_cpu time=0` | An error: the window must be at least one second |
| A threshold or unit that overflows (`used > 1.0e30T`, `time=5000000w`) | An error instead of a wrapped-around value |
| A module that failed to load | Dropped from the module list; no longer answers `exec` |
| `NSClientServer` (check_nt) or `CheckMKServer` on a settings reload | Restart their listener so a changed port or password takes effect; open connections drop |
| A Python script unloading `PythonScript` from inside | Refused |

### ⏱️ CheckSystem and CheckDisk — shutdown no longer waits on Windows Update or WMI

Stopping the service shortly after it started could take minutes on Windows
(#1504). The first Windows Update check the agent runs goes online to Windows
Update or WSUS and cannot be interrupted, and the service waited for it. The
WMI queries behind the network, temperature, CPU frequency, battery and disk
I/O collectors could hold things up the same way while the WMI performance
service restarts. All of them are now abandoned when the service stops.

### 🐧 Building from source

The tree builds with GCC 16 (Debian unstable, Fedora rawhide), which defaults
to C++20 (#1479).

### 📚 Documentation

- New scenario: [Polled Passive Checks (Nagios Core)](https://nsclient.org/docs/scenarios/nagios-result-cache/).
- New REST page: [Results](https://nsclient.org/docs/api/rest/results/).
- New extending page: [.NET plugins](https://nsclient.org/docs/extending/dotnet/).
- The WEB server reference covers the new `/settings/WEB/server/results` section.

## ⚠️ Upgrade notes

- 🔒 **Check the permissions of certificates the agent generated for you.**
  The upgrade does not touch existing files: run
  `chmod 600 /etc/nscp/security/certificate.pem` (or restrict the file to the
  service account on Windows). If you handed out a generated `ca.pem`,
  regenerate that CA and re-issue client certificates — the old file contains
  the CA's private key.
- 🔒 **If `dh` names `nrpe_dh_512.pem`, change it before upgrading** to
  `${nrpe-dh}/nrpe_dh_2048.pem`; the file is no longer shipped and the
  listener will otherwise fail to start. An existing copy on disk is left
  where it is.
- 🔒 **The NRPE client logs an error for every target it does not
  authenticate.** The default (`verify mode = none`) is unchanged. Set
  `verify mode = peer-cert` with `ca` pointing at the issuer to authenticate
  the server and silence it. Regenerate an existing generated certificate to
  get one that can be verified.
- 🔒 **Slow clients may be dropped during the TLS handshake.** The handshake
  now has to finish within the listener's `timeout` (30 s by default). Raise
  `timeout` if a client on a slow link stops connecting.
- 🔒 **A credential inside a target's `address` now blocks `host=` overrides**,
  as one in `password` or `token` already did. Use `target=`, pass the
  credential with the request, or set `allow host override = true`.
- 🔒 **Some inputs that used to misbehave are rejected**: see the table above.
  Nothing to do unless you relied on one of them.
- 🔌 **`DotnetPlugins` is available again** but not loaded unless you add
  `DotnetPlugins = enabled` under `[/modules]`, and it needs a .NET runtime
  (8.0 or newer) installed on the host. Plugins built against the old .NET
  Framework `NSCP.Core.dll` must be rebuilt against the new one.
- 📤 **The result cache is off by default.** Enabling it needs a service
  restart, and the account that polls needs the `results.*` privileges. The
  bundled `check_nsclient` is now 1.1.0; existing invocations are unaffected.
- 🔧 **Every documented `tls version` spelling works now.** Nothing to do; the
  default `tlsv1.2+` was never affected.

Full detail on the security items lives in [Security notices](https://nsclient.org/docs/security/notices/); the operator
actions are mirrored on [Upgrading](https://nsclient.org/docs/setup/upgrading/).


## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.20.0){ .md-button }

// Michael Medin

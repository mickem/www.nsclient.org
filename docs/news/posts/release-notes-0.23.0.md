---
date:
  created: 2026-09-22
---

# 0.23.0 Paths that land where you meant them, more enforced TLS verification, and logins that survive a restart

0.23.0 is a short release with two themes, and both are about a setting that
looked right and did something else.

The first is paths. Expanding a path substituted `${tokens}` and never made
anything absolute, so a bare relative name was measured against the process's
working directory — `C:\Windows\System32` for a Windows service, `/` under a
bare init script, the shell's directory for `nscp test`. An unrecognised token
was not an error either: `${scripst}/check.bat` quietly became a real path
under the installation folder, and whatever depended on it went somewhere
nobody was looking. A relative value in a setting that writes files now lands
in the folder that setting owns, an unknown token is reported and the setting
skipped, `file name = none` really switches the log off, and on Windows a
relative external-script command is found from where it is rather than from
where `nscp` was started.

The second is TLS verification, in the three places where it was configured
but not happening. A listener `verify mode` parser accepted five spellings and
silently dropped everything else — including `fail-if-no-peer-cert`, the
spelling the documentation tells you to write — so a carefully configured
mutual-TLS listener was really a listener with an IP filter. The NSCP and
check_mk clients, and `check_nsclient_web_online`, encrypted their connections
and never authenticated the peer. And a fleet `mtls_url` that was not
`https://` ran the whole management channel — desired state, signed bundles,
certificate renewal — on a plain socket, with the client certificate and the
pinned CA doing nothing. All three now fail closed, which means three of this
release's notes need reading before you upgrade.

Then the smaller things: you stay logged in to the web UI across a restart,
session tokens are only ever held as hashes, a multi-adapter Windows host stops
publishing every NIC's metrics twice, and non-ASCII text in the UI and the
reference docs is no longer mojibake.

## ✨ Highlights

- 🔒 **A listener `verify mode` it does not recognise now refuses to start.**
  `verify mode = peer,fail-if-no-peer-cert` resolved to bare `peer`: the
  listener asked for a client certificate and completed the handshake when none
  arrived. Both spellings are accepted now, along with `certificate` and
  `client-certificate`, and any other token makes the listener log it and stop
  instead of starting with whatever survived the typo. **Check every listener
  you have configured for mutual TLS before upgrading.** (#1555)
- 🔑 **The NSCP and check_mk clients, and `check_nsclient_web_online`, verify
  the server certificate by default.** All three encrypted the connection and
  authenticated nothing, while sending the remote agent's password over it.
  `verify mode` / `verify` now defaults to `peer` and `ca` to the agent's own
  trust bundle; a target pointed at an agent still using its self-signed
  certificate needs `ca = <that certificate>` and `verify mode = peer-cert`.
  (#1568)
- 🛰️ **A fleet management url that is not `https://` is refused**, and
  enrollment no longer follows a symlink planted by the service account. The
  `mtls_url` carries configuration and signed bundles, which is remote code
  execution by design; on a plain socket neither the agent's client certificate
  nor the pinned server certificate did anything. `nscp enroll --insecure`
  records the decision where plaintext is genuinely wanted. (#1555)
- 🗂️ **A relative path in a setting that writes files is rooted at the folder
  that setting owns.** The log file lands in `${log-path}`, an attachment in
  `${shared-path}`, a crash archive in `${crash-folder}`, a fleet managed path
  in `${fleet-folder}`, a filewriter log in `${log-path}` — instead of in
  whatever the service's working directory happened to be. (#1560)
- 🚫 **An unknown `${...}` path token is an error, and a `[paths]` override has
  to name a location of its own.** A mistyped token used to resolve to the
  installation directory; now the setting that carried it is skipped and the
  log says which token and which setting. `file name = none` switches the log
  off on Windows too, where it used to create a file called
  `C:\Program Files\NSClient++none`. (#1560)
- 🪟 **A relative external-script command is found from where it is, not from
  where `nscp` started.** `check_foo = scripts\check_foo.bat` worked or failed
  depending on how it was spelled: an argv-safe spelling resolved against the
  service's working directory and failed with "the system cannot find the path
  specified". It is rooted at the installation directory now, both ways. (#1560)
- 🔐 **You stay logged in to the web UI across a restart, and a session token is
  only ever held as a hash.** Restarting or upgrading the agent no longer logs
  every web user out; only the SHA-256 of each key is kept, in memory and on
  disk, and a logout removes it immediately. `persist sessions = false` brings
  back the old behaviour. (#1549, #1573)
- 📥 **`ext-scr`, `py` and `lua` `add --import` work on a fresh install and
  record a path that resolves.** The destination folder is created, the
  recorded value resolves on both platforms, and an import with no `--script`
  is refused instead of overwriting the script folder with a file. The Web UI's
  script upload goes through the same path. (#1560, #1557)
- 🔁 **Remote `[/includes]` and `[/attachments]` refresh on their own.** An
  agent configured from an `http(s)://` settings url re-read only the top-level
  file on each maintenance pass, so an included file stayed pinned to whatever
  it held at start. Both are fetched every pass now, and a change in either
  triggers the same reload. (#1560)
- 🛡️ **The op5 installer profile defaults to secure NRPE**, and the Windows
  release build verifies what it downloads. The op5 page used to force legacy
  mode, hide the radio group so the choice could not be seen, and enable
  `allow nasty characters`; the dependency checksum file added last release had
  every line reading `unrecorded`. (#1555)

## 🔍 Detailed changes

### 🗂️ Paths — resolved against something that does not move

Expanding a path substituted `${tokens}`; it never made anything absolute. A
value with neither a token nor a leading `/` was therefore resolved against
whatever the service's working directory happened to be — four different
answers from the same configuration file, depending on how the agent was
started.

**A relative value lands in the folder its consumer owns.**

| Setting | Relative values now land in |
|---|---|
| `[/attachments]` target | `${shared-path}` |
| `[/settings/log] file name` | `${log-path}` |
| `[/settings/crash] archive folder` | `${crash-folder}` |
| `[/settings/fleet] managed path` | `${fleet-folder}` |
| `[/settings/filewriter] file` | `${log-path}` |

On unix this usually changes nothing, because the working directory and the
package directory tended to agree. On Windows it moves a file that was landing
in `C:\Windows\System32` into the folder it should always have been in.

**An unknown token is reported and the setting skipped.** The tokens stay open
ended — anything defined in `boot.ini`'s `[paths]` section counts as known —
but `${scripst}/check.bat` is now an error in the log rather than a real path
under the install folder that nobody is watching. `${appdata}` and
`${common-appdata}` are Windows-only and are rejected on unix, where they
previously resolved to the installation directory.

**A `[paths]` or `--path-override` entry that does not resolve to a location of
its own is ignored**, with an error naming it, and the built-in default
applies. An override may still be written in terms of other tokens
(`scripts = ${shared-path}/mine`); it is the resolved value that is judged.
"A location of its own" is slightly wider than "absolute": a drive-relative
`C:mine` and a root-relative `\mine` are accepted on Windows, because the
operator plainly named a drive or a root.

**`none` is a sentinel the path expander knows.** `[/settings/log] file name =
none` is documented as "no log file", but the name was joined to the
installation directory before the sentinel was tested — so on Windows it
produced a real file called `C:\Program Files\NSClient++none` and file logging
stayed on. It is recognised by the expander itself now, so it is equally safe
in every setting that accepts it, including every `ca` option where it means
"use the TLS library's own trust store". (#1560)

### 🪟 Windows: external scripts, found from where they are

`[/settings/external scripts/scripts]` entries that carry a folder — the
conventional `check_foo = scripts\check_foo.bat`, and what
`nscp ext-scr add --import` writes — are rooted at `${base-path}` before they
are launched.

The old behaviour was easy to miss because it depended on how the command
happened to be spelled. A single backslash is not tokenisable as an argument
vector, so it fell back to the legacy single-string launcher, where the lookup
already honoured the installation directory and the command worked. A command
that *was* argv-safe — a doubled backslash, a forward slash, a quoted path —
ran with argv isolation, where the executable is named separately and was
resolved against the working directory, and it failed for the service with
"the system cannot find the path specified".

Absolute paths, UNC paths, drive-relative `C:check.exe` and root-relative
`\tools\check.exe` are all still used exactly as written. (#1560)

### 📥 Script folders and imports

Both ext-scr CLIs derived their folder by appending a literal `scripts`
segment to a root rather than naming `${scripts}`, the token that already means
that folder:

| | Looked in / imported into (before) | Now |
|---|---|---|
| `nscp lua list/show/add/delete` | `${base-path}/scripts/lua` — right on Windows, `/usr/sbin/scripts/lua` on Linux | `${scripts}/lua` |
| `nscp py list/show/add/delete` | `${scripts}/scripts/python` — a folder nothing creates | `${scripts}/python` |

`add --import` also records a different value: `python/<name>` and `lua/<name>`
relative to `${scripts}`, instead of the `scripts\python\<name>` spelling that
only resolved on Windows.

Three things were wrong with importing a script, each silent in its own way.
`copy_file` never created the destination folder, so a fresh install died with
a bare *No such file or directory*; `ext-scr` recorded a Windows spelling of a
path it never resolves, so the imported command exited 127 on Linux; and
`add --import` with no `--script` collapsed the destination onto the script
folder itself and overwrote it with a file. The folder is created, the recorded
path is absolute on Linux, and the missing option is named. The Web UI's script
upload goes through the same `add --import` and failed the same way.

**The Windows installer creates `scripts\custom\` again, and always.** It is
not part of the *Scripts* (`SampleScripts`) feature, so `REMOVE=SampleScripts`
no longer leaves an installation with no `scripts\` directory at all — which
previously meant an `[/attachments]` entry, or anything else writing a script,
had nowhere to land. (#1560, #1557)

### 🔁 Remote includes and attachments

An agent configured from an `http(s)://` settings url re-downloads its whole
configuration every *settings maintenance interval* (default `5m`). Until now
that pass stopped at the top-level file: a file pulled in by `[/includes]`, and
every `[/attachments]` target, was only re-fetched when the top-level file
itself happened to change. On a server where `nsclient.ini` is the stable part
and the included file is the one that moves, the include stayed pinned to
whatever it held when the agent started.

Both are fetched on every pass now, and a change in either triggers the same
reload a change in the top-level file does. Two things to be aware of: the
settings server sees one request per included file and per attachment on every
interval (responses are hash-compared, so an unchanged file costs only the
request), and a change made only in an included file now takes effect within
one interval instead of requiring a restart. (#1560)

### 🔒 TLS verification that was configured but not happening

**Listeners.** The `verify mode` parser accepted five spellings and silently
ignored everything else. `fail-if-no-peer-cert` was not one of the five — but
it is what the permissions guide, the `client identity source` help text,
OpenSSL itself, the NRPE scenario walkthrough and the reference docs all tell
you to write. So `verify mode = peer,fail-if-no-peer-cert` resolved to bare
`verify_peer`: the listener asked the client for a certificate and completed
the handshake when none arrived. An operator whose configuration looked exactly
like the documentation was running an NRPE listener authenticated by the
`allowed hosts` IP list alone, and any typo degraded the same way, always in
the direction of accepting more.

The parser now takes the same vocabulary as the outbound client parser —
`peer` or `certificate`, `fail-if-no-cert` or `fail-if-no-peer-cert` or
`client-certificate`, plus `peer-cert`, `client-once`, `none`, and the context
options `workarounds` and `single` — and ignores whitespace around a token.
Anything else is rejected: the listener logs the offending token and does not
start.

**Outbound clients.** `NSCPClient` defaulted `verify mode` to `none`,
`CheckMKClient` left it unset (an empty verify mode parses the same as `none`),
and `check_nsclient_web_online` defaulted `verify` to `none`. All three sent
the remote agent's password over a connection whose peer was never
authenticated. `verify mode` / `verify` defaults to `peer` now and `ca` to
`${ca-path}` — the auto-generated ROOT store export on Windows, the
distribution bundle elsewhere.

Because an agent generates a **self-signed** certificate on first start, a
relay or REST check pointed at a default agent will now fail the handshake
where it used to connect:

| Situation | Configuration |
|---|---|
| The remote agent uses a certificate from your own CA | `ca = <the CA>` (the default `verify mode = peer` then works) |
| The remote agent still uses its self-signed certificate | `ca = <that certificate>` and `verify mode = peer-cert` |
| You accept an unauthenticated link | `verify mode = none` (encrypted, but an on-path attacker can impersonate the remote) |

**Fleet.** The enrollment response names `mtls_url`, the base for the
desired-state poll, the bundle download and the certificate renewal. The
fail-closed guard that refuses mTLS without server authentication only existed
on the TLS path, so a response carrying `http://…` — or a url with no scheme,
which the http client also opens on a plain socket — built a plain TCP client,
ignored the certificate and the pin, and ran the whole management channel
unauthenticated with nothing in the log to say so. Enrollment refuses a
non-https management url, the sync loop refuses to start on a stored one, and
the http client refuses to attach a client certificate or a pinned CA to a
non-TLS transport at all. `nscp enroll --insecure` and `[tls] allow plaintext =
true` record the decision; the sync then logs `INSECURE` on every start.

Enrollment's two pre-`adopt_owner` writes also followed symlinks. The manifest
temporary and the `fleet.ini` placeholder were created with a plain `open` and
a plain `ofstream` in a directory the unprivileged service account owns, so
that account could pre-create either name as a link and have the next
`sudo nscp enroll` truncate the target as root. Both now open the containing
directory `O_NOFOLLOW|O_DIRECTORY` and create through that descriptor with
`O_CREAT|O_EXCL|O_NOFOLLOW`.

**The op5 installer profile.** Picking **op5** on the MSI's monitoring-tool
page used to force NRPE into legacy mode — anonymous Diffie-Hellman, no peer
verification — hide the mode radio group so the choice could not be seen or
changed, and enable `allow nasty characters` for every NRPE-reachable check.
It now defaults to the same secure mode the generic profile uses, shows the
radio group so legacy is a visible decision, and does not set `allow nasty
characters`. `allow arguments` stays on, because op5's check commands need it.
(#1555, #1568)

### 🔐 Web sessions

Restarting the service, or upgrading it, no longer logs every web user out: a
browser tab, and a script holding a key from `/api/v2/login`, keeps working.
Sessions are kept in `${data-path}/nsclient.db` and restored at the next start,
still expiring eight hours after login.

Only the SHA-256 of each session key is stored, in memory and on disk, so a
copy of the database — or a dump of the process — does not yield a usable
token. A session is only restored while the user's password and role are
unchanged, and logging out removes it from the file straight away; it stops
working immediately and does not come back, not even if the agent is killed
rather than stopped cleanly.

Changing a user's password or role also ends that user's sessions, and removing
the user ends theirs — but only from the next start of the agent, because the
running service keeps the users it read when it started.

`persist sessions = false` under `[/settings/WEB/server]` keeps sessions in
memory only, as before. It is also the way to invalidate every session at once
after a suspected leak: restart once with it off. (#1549, #1573)

### 🐛 Bug fixes

- **A Windows host stops publishing every network adapter's metrics twice.**
  `check_network`'s two source maps both hold every adapter
  `Win32_NetworkAdapter` knows about, and `fetchMetrics` handed both copies to
  the bundle under the same key. The JSON views kept whichever came first and
  dropped the other silently; the OpenMetrics renderer refused the duplicate
  series and logged one error per field per snapshot — on a five-adapter host,
  70 error lines on every metrics tick. (#1575)
- **Non-ASCII text is no longer mangled into mojibake.** UTF-8 read as cp1252
  and re-encoded as UTF-8 stays valid UTF-8, so nothing downstream complained:
  the module-glue generators read `module.json` with a bare `open()`, so an em
  dash in a command description was doubled by a Windows builder and carried
  into the registry, the REST API, `nscp test desc` and the extracted reference
  docs. Eight user-visible strings are repaired. (#1576)
- **WinGet publishing works again.** The manifests were bumped to schema 1.12.0
  for 0.21.0, which the in-box winget on the runner does not ship, so
  validation failed on a schema header mismatch and both releases went
  unsubmitted. The header and `ManifestVersion` are back to 1.9.0, and the
  publish step reads the exit code instead of dying on the warning-only
  result. (#1572)
- **The Windows release build verifies what it downloads.** The checksum gate
  added last release was in place but every line in
  `.github/dependency-checksums.txt` read `unrecorded`, so each download warned
  and continued. Digests are recorded for OpenSSL, protobuf, Crypto++, miniz
  and the prebuilt `check_nsclient.exe`; TinyXML2, Mongoose and MariaDB
  Connector/C are cloned and verified against a recorded commit rather than
  fetched as GitHub-generated tag archives. Bumping a dependency now means
  adding its line first, because a missing line fails the build. (#1555)

## ⚠️ Upgrade notes

- **Check the `verify mode` of every listener configured for mutual TLS before
  upgrading.** A token this release does not recognise makes the listener log
  it and refuse to start — which is the point, but it is a restart away. If you
  believed a listener was requiring client certificates, verify it now: until
  this release, `fail-if-no-peer-cert` was dropped and the handshake completed
  without one.
- **An `NSCP` or `CheckMK` client target, or a `check_nsclient_web_online`
  check, pointed at an agent with its self-signed certificate will now fail the
  handshake.** Set `ca = <that certificate>` with `verify mode = peer-cert`,
  point `ca` at your own CA, or accept an unauthenticated link explicitly with
  `verify mode = none`.
- **A fleet host enrolled against a plaintext `mtls_url` stops syncing.**
  Re-enroll against `https://`, or record the decision with
  `nscp enroll --insecure` / `[tls] allow plaintext = true` in `boot.ini`.
- **An op5 host monitored by a `check_nrpe` with no client certificate needs
  one**, or **Insecure mode** picked explicitly on the installer's
  monitoring-tool page. The profile no longer forces legacy NRPE, and no longer
  sets `allow nasty characters`.
- **A bare relative path in a setting that writes files moves** — on unix
  usually not at all, on Windows usually into the folder it should always have
  been in. Nothing to do if your paths are absolute or written with `${...}`
  tokens.
- **An unrecognised `${...}` token, and a `[paths]` override that does not
  resolve to a location of its own, are now errors** that skip the setting
  instead of quietly resolving to the installation directory. `${appdata}` and
  `${common-appdata}` are rejected on unix.
- **If `[/settings/log] file name = none` was set on Windows**, a stray file
  called `C:\Program Files\NSClient++none` is left where it is — delete it once
  you have checked you do not need its contents.
- **A relative external-script command that relied on the working directory no
  longer resolves.** Name the script with an absolute path, or with
  `${scripts}\<name>`. An absolute, UNC, drive-relative or root-relative
  command is unaffected.
- **`nscp lua` and `nscp py` look in a different folder**, and record a
  different value on import. Existing configuration entries keep working and
  loading scripts from `nsclient.ini` is unchanged.
- **If you relied on a restart to log every web user out**, set
  `persist sessions = false` under `[/settings/WEB/server]`.
- **A settings server now sees one request per included file and per attachment
  on every maintenance interval.** Responses are hash-compared, so an unchanged
  file costs only the request — but size the interval accordingly if you serve
  a large attachment to a large fleet.

Security notices for this release are on the
[security notices page](https://nsclient.org/docs/security/notices/), and the
full list of behaviour changes is on the
[upgrading page](https://nsclient.org/docs/setup/upgrading/).

## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.23.0){ .md-button }

// Michael Medin

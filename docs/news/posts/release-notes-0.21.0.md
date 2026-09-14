---
date:
  created: 2026-09-14
---

# 0.21.0 NSClient Fleet launches: central management for your agents, plus checks that only read what you allow

0.21.0 is the agent release that goes with the first release of **NSClient
Fleet**, a new, separate product: one server that holds the configuration for
a whole estate of NSClient++ agents, hands each host the part that applies to
it, and shows you what every host is actually running. Agents enroll
themselves and report what they are, so the server builds the inventory
instead of consuming one; groups select hosts by those reported tags, and
bundles of configuration and scripts attach to groups. This release brings
the agent side to feature parity with the server: encrypted bundles the server
cannot read, a way to leave a fleet, and an `nscp test` prompt that survives a
configuration push. Fleet is entirely optional; NSClient++ works exactly as it
always has without it.

The other theme is reading less. `check_logfile`, `check_files`, `check_wmi`,
`check_pdh`, `check_registry_*` and `check_eventlog` read whatever their
argument names, with the agent's privileges, which is a general read primitive
wherever a caller may choose the argument. Each of them now has an access mode
and an allow list, off by default. Two WEB roles complete the picture:
`restricted` runs the checks you define but passes no arguments, and
`metrics` scrapes and does nothing else. And the `nscp test` prompt got a
round of usability work: aligned listings, a `desc` that shows defaults and
what an alias runs, filter keyword lists, single-quoted paths and
case-insensitive completion.

## ✨ Highlights

- 🚀 **NSClient Fleet is out.** A server that enrolls your agents, builds the
  inventory from what they report, and delivers configuration and scripts per
  host as signed bundles, pulled by the agent over mTLS with no inbound port.
  Read the [launch announcement](https://nsclient.org/news/2026/09/14/nsclient-fleet/)
  and the [Fleet documentation](https://nsclient.org/docs/fleet/); this
  release is the agent side of it.
- 🛡️ **Access modes for the checks whose argument decides what is read.**
  `check_logfile`, `check_files`, `check_single_file`, `check_disk_write`,
  `check_wmi`, `check_pdh`, `check_registry_key`, `check_registry_value` and
  `check_eventlog` each gained a mode setting and an allow list. The default,
  `any`, is exactly the previous behaviour; `predefined` limits a caller to the
  names you configured; `allowed` matches an allow list. Nothing changes on
  upgrade. (#1516)
- 🔒 **Two WEB roles that cannot be widened.** `restricted` holds
  `queries.execute.noargs`, the REST equivalent of NRPE's
  `allow arguments = false`: it runs the checks the agent defines and refuses
  any query-string parameter. `metrics` reads the two metrics endpoints and
  nothing else. The bundled `monitoring` role finally holds the grant the
  metrics endpoints actually check, so a monitoring user is no longer answered
  403 there. (#1517, #1520)
- 🔐 **Encrypted fleet bundles.** A bundle sealed in the fleet server's browser
  is opened by the agent with a key you hand it out of band, at enrollment
  (`nscp enroll --bundle-key`, `FLEET_BUNDLE_KEY` on the MSI) or later. The key
  and the optional "sealed bundles only" posture live in the enrollment
  manifest, never in the settings store, so the server cannot plant or switch
  them. (#1521)
- 🚪 **`nscp enroll --unenroll` leaves the fleet.** It removes the include,
  the identity and keys, and the fleet directory, and reports each step.
  (#1521)
- 💥 **`nscp test` no longer crashes after a fleet configuration push.** A
  settings reload replaced the object the prompt's completion held a pointer
  to; the next completion refresh dereferenced freed memory. The crash file the
  agent writes now names the faulting module instead of printing a pointer.
  (#1521)
- 🖥️ **A better `nscp test` prompt.** Padded tables instead of tabs in every
  listing, `desc` with parameter defaults, the bare-call command line and what
  an alias runs, a `keywords` verb listing a check's filter keywords, `alias`
  as a shorter `aliases`, Tab completion that corrects `load check` to
  `load Check…`, single quotes that take paths literally, `exec` that passes
  `--options` to a module, and a `settings` dump that lists only what is
  configured with passwords masked. (#1522)
- 🔎 **Three follow-up fixes to the access gates from review**, including a
  path written with the other separator walking out of an allowed directory,
  a link the path resolver skipped, and a reload window during which every
  gate stood open. Ship the release with those in, not the first cut.
- 📦 **Packaging.** Each Windows install no longer strands an 8 MB copy of
  `nscp.exe` under `%WINDIR%\Installer`, the WinGet manifests carry the
  metadata the upstream validator wants again, and the Debian source package
  drops a Unicode-licensed file so it passes Lintian. (#1518)

## 🔍 Detailed changes

### 🚀 NSClient Fleet

Until now a large estate of agents was configured either by pointing each one
at an ini file on a web server or by pushing settings over the REST API from
whatever orchestration you already run. Both still work. Neither keeps track
of the estate: the only inventory is the one you maintain by hand.

Fleet turns that around. A host enrolls with a one-time token, a few MSI
properties or one `nscp enroll` command, and appears in the inventory with its
OS, version, drives and detected roles as tags the agent reported. Groups
select hosts by tag, bundles of INI fragments and scripts attach to groups,
and each host pulls the bundles that apply to it, verifies their signatures,
renders them into a `fleet.ini` its own `nsclient.ini` includes, and reports
back what it applied. The server never pushes and never needs a port opened on
a monitored host. Status is derived from what hosts report: in sync, out of
sync, offline, lost, and whether local settings outrank what the server sends.
It is one static binary and a SQLite file, on Linux or Windows or as a
container, in [its own repository](https://github.com/mickem/nsclient-fleet-server).

To learn more, start with the
[launch announcement](https://nsclient.org/news/2026/09/14/nsclient-fleet/),
then the [Fleet documentation](https://nsclient.org/docs/fleet/) for running
it in Docker, installing it on Linux or Windows, and the deployment reference.
The agent-side walkthrough is
[Central management with NSClient Fleet](https://nsclient.org/docs/setup/fleet/).
What this release adds on the agent side is below.

### 🛡️ Restricting what a check may read

The checks in the table take an argument that decides *what data is read*,
and the agent reads it with its own privileges. Where callers choose the
argument, NRPE with `allow arguments = true` or a REST user not on the
`restricted` role, an unrestricted `file=` is a general file-read primitive.
Each module gained a mode setting and an allow list:

| Check | Section | Mode setting | Allow list |
|-------|---------|--------------|------------|
| `check_logfile` | `[/settings/logfile]` | `file access` | `allowed files` |
| `check_wmi` | `[/settings/wmi]` | `query access` | `allowed classes`, `allowed namespaces` |
| `check_pdh` | `[/settings/system/windows]` | `counter access` | `allowed counters` |
| `check_files`, `check_single_file`, `check_disk_write` | `[/settings/disk]` | `file access` | `allowed files` |
| `check_registry_key`, `check_registry_value` | `[/settings/system/windows]` | `registry access` | `allowed registry keys` |
| `check_eventlog` | `[/settings/eventlog]` | `log access` | `allowed logs` |

The modes are `any` (the default, and what every earlier release did),
`predefined` (the secure option: only names you configured in the module's own
sections, such as `[/settings/logfile/files]` or the counters already in
`[/settings/system/windows/counters]`) and `allowed` (only what matches the
list; experimental, since it has to parse what the caller sent). Registry and
event-log entries are hierarchical and match whole name segments. Configured
names resolve in every mode, so you can name your checks first and tighten
the mode afterwards.

Once a mode is set, some arguments tighten with it: a `check_wmi` `namespace=`
may no longer leave `root\cimv2` unless `allowed namespaces` says so and its
`target=` must name a configured target, `check_registry_*` refuses
`computer=`, and `check_eventlog`'s default channels go through the gate like
any other. Review of the gates before release closed a path written with the
other separator walking out of an allowed directory, a symbolic link the path
resolver did not follow, a NUL byte, a remote host in the path, and a window
during a settings reload in which every gate stood open; `allowed` mode judges
a WMI query by its class rather than its text. Alongside this, `check_files`
on Windows no longer follows file symbolic links, as the Linux scanner never
did, and `*` and `?` in a path allow list no longer cross a directory
separator (`C:/logs/**.log` for the subtree). See
[Restricting what a check may read](https://nsclient.org/docs/concepts/check-access/).

### 🔒 WEBServer — roles that cannot be widened

`restricted` holds `queries.execute.noargs` instead of `queries.execute`: the
caller may run the checks the agent defines, and a request carrying any
query-string parameter is refused with `403 Arguments are not allowed for this
user`. Neither grant implies the other. Give such a caller the checks that
need arguments as aliases, so the arguments live in your configuration:

```ini
[/settings/WEB/server/users/monitor]
role = restricted

[/settings/check helpers/alias]
check_root_disk = check_drivesize drive=/ warning=free<10% critical=free<5%
```

Every query parameter counts, including a session token passed the legacy way
as `?TOKEN=`, so a restricted client authenticates with a header.

`metrics` is for a Prometheus scraper: `metrics.list` and `openmetrics.list`,
no `queries.execute`. The bundled `monitoring` role granted `metrics.get`, a
privilege nothing checks, so a monitoring user got 403 on both metrics
endpoints; it now grants the two real ones. Roles already written to
`nsclient.ini` are never rewritten, so an existing `monitoring` line keeps its
inert grant until you update it or assign `metrics` instead.

### 🔐 Fleet — encrypted bundles and unenrolling

A bundle the operator seals in the fleet server's browser (`format: enc-v1`)
used to be refused by the agent as an unreadable archive. The agent now opens
it. The envelope is AES-256-GCM with the bundle's name and version bound in as
additional data, so a server that re-labels an old sealed bundle gets a
refusal; the published checksum and signature cover the envelope, so download
verification is unchanged and decryption is a step after it. The plaintext
exists on disk only while it is unpacked; the cache keeps the envelope.

The key reaches the host out of band, never from the server:

| Where | How |
|---|---|
| At enrollment | `nscp enroll --bundle-key <key>` (repeatable while rotating), or `FLEET_BUNDLE_KEY=<key>` on the MSI |
| On an enrolled host | `nscp enroll --update-bundle-keys --bundle-key <key>`, or re-run the MSI with only `FLEET_BUNDLE_KEY` |
| Sealed bundles only | `nscp enroll --require-encrypted-bundles`, or `FLEET_REQUIRE_ENCRYPTED_BUNDLES=1` |

Both the keys and the requirement are stored in the enrollment manifest
beside the host's private key, not in `nsclient.ini`: the fleet-managed
configuration is an include of the settings store, so anything kept there
could be planted by the very server the bundles are sealed against. A bundle
sealed with a key the host lacks is refused and the state report names the
missing key's fingerprint, which is what the server shows on its key page.

`nscp enroll --unenroll` removes the `[/includes] fleet` entry, the manifest
and the fleet directory, in that order, and says what it removed; a service
restart stops the sync. It is a local act, so remove the host on the server as
well. Enrollment also resolves the manifest path from `[/settings/fleet]`
`state file` on every path now; a host that sets that key used to enroll into
a file the service never read. See
[Central management with NSClient Fleet](https://nsclient.org/docs/setup/fleet/),
new in this release as a guide. (#1519, #1521)

### 🖥️ The `nscp test` prompt

A fleet configuration push, or any settings reload, killed the prompt: the
reload re-entered the module and replaced the client object the completion
hooks held a raw pointer to. Fixed, and the crash record the agent writes now
names the faulting module (it printed a pointer). On top of that:

| Verb | Now |
|---|---|
| `queries`, `aliases`, `list`, `plugins` | Padded tables, one line per entry; `list` really lists both kinds |
| `desc <query>` | Parameter defaults, the command as it runs bare (`show-default`), and for an alias the command it runs plus that command's parameters |
| `keywords <query>` | The filter keywords and functions of a check with their descriptions, from the running agent |
| `alias` | Same as `aliases` |
| `settings` | Only what the configuration sets, with passwords masked |
| `exec <module> --opt` | Options reach the module as `nscp <module> --opt` sends them, instead of `--opt` being taken for the command |
| `load check<Tab>` | Completes and corrects the case: `CheckDisk`, `CheckSystem`, … |
| `'C:\Program Files\x'` | Single quotes take their content literally; `"..."` keeps its backslash escapes, and `filter=core='total'` typed bare still reaches the check as written |

A PDH enumeration race seen through `exec CheckSystem --list` inside the
prompt is fixed as well: when the counter list grows between the sizing call
and the fetch, the agent grows the buffer and retries instead of reporting
`PDH_MORE_DATA` as a failure. (#1522)

### 🐛 Bug fixes

- `check_logfile files=` works: the comma-separated form was parsed before
  the check read its arguments and had been ignored since it was added; it is
  one list with `file=` now, and every name goes through `file access`.
- `check_installed_software` on Debian and Ubuntu takes install dates from
  `dpkg-query` (`db-fsys:Last-Modified`, dpkg 1.19.3 or later) instead of
  dpkg's internal database, and returns UNKNOWN when a package's file list
  cannot be read for a reason other than a missing file. (#1485)
- The `nscp test` fallback on Linux appended a tab and `...` to every line of
  multi-line output; it now prints the record as written, as Windows did.
- Enrolling with a bundle key that has `=` padding in the middle is refused
  with a message that says so, and the MSI names the property that is
  actually missing when only `FLEET_REQUIRE_ENCRYPTED_BUNDLES` is given on an
  unenrolled host.

### 📦 Packaging

- The MSI's Add/Remove Programs icon was `nscp.exe` itself, so Windows
  Installer extracted an isolated 8 MB copy of the agent into
  `%WINDIR%\Installer` on every install. It is a real icon now.
- The WinGet manifests declare the VC runtime dependency, the real licence,
  the published moniker, `ReleaseNotes`, `Documentations`, locale, scope and
  installer switches again, date a manually re-published manifest by its
  release rather than the day the workflow ran, and keep the useful part of
  the release notes instead of cutting a table in half.
- The vendored replxx used by the prompt no longer carries Unicode, Inc.'s
  `ConvertUTF`, whose licence is not DFSG-free; the Debian source package
  passes Lintian again. (#1518)

## ⚠️ Upgrade notes

- **Nothing changes by itself.** Every access mode defaults to `any`, no user
  is assigned to the new WEB roles, and roles already written to
  `nsclient.ini` are not rewritten. Set a mode, or update a `monitoring` role
  line, only when you want the new behaviour.
- **`check_files` on Windows skips file symbolic links.** If you relied on
  them being counted, point the check at the link targets. Path allow-list
  wildcards no longer cross directory separators; use `**` for a subtree.
- **`check_logfile` with both `file=` and `files=` reads the union** from
  this release on. Nothing to do unless you relied on `files=` being dropped.
- **`check_installed_software` on a dpkg older than 1.19.3** leaves
  `install_date` unset, so an expression on it no longer matches there.
- **Encrypted fleet bundles need the key on every host** before the server
  starts serving sealed bundles; a host without it refuses them and names the
  missing key's fingerprint in its state report. There is no key escrow on
  the server.

Security notices for this release:
[Access modes for the checks whose argument decides what is read](https://nsclient.org/docs/security/notices/),
[WEB: a metrics role, and a corrected metrics grant on the monitoring role](https://nsclient.org/docs/security/notices/),
[Fleet: encrypted bundles are opened by the agent, not the server](https://nsclient.org/docs/security/notices/) and
[Sensitive settings are redacted in the nscp test settings dump](https://nsclient.org/docs/security/notices/).
The full list of behaviour changes is on the
[upgrading page](https://nsclient.org/docs/setup/upgrading/).

## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.21.0){ .md-button }

// Michael Medin

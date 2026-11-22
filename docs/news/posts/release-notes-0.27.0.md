---
date:
  created: 2026-11-22
---

# 0.27.0 Failed checks that explain themselves, a native Icinga 2 agent, and a Checkmk agent that matches the official one

0.27.0 is about the moment a check fails. The agent now keeps a log of its last failed checks, and can keep the metrics and diagnostics tables (top processes, services in trouble, the last log errors, the usual disk growth spots) from that moment, on the host and for the fleet server. It also adds an experimental `IcingaAgent` module that joins an Icinga 2 cluster natively, brings the Checkmk agent dump in line with the official agent, and adds pressure metrics, per-volume growth, and Hyper-V over-commitment and switch checks.

## ✨ Highlights

- 🧾 **A log of the last failed checks.** The core keeps the last 50 WARNING, CRITICAL and UNKNOWN results from every transport, with output and perfdata. It shows on a new *Failed checks* page, as a dashboard widget and at `GET /api/v2/failures` (#1697).
- 🔍 **What the system looked like when it failed.** With `capture metrics` and `capture diagnostics` on, each failure keeps the metrics snapshot and small diagnostics tables from that moment. A new *Diagnostics* page shows them live, and an enrolled agent can send failure context to the fleet server (#1699, #1710).
- 🧊 **`IcingaAgent`: NSClient++ as a native Icinga 2 agent (experimental).** It speaks the cluster protocol on port 5665, requests its certificate from the Icinga CA and runs the checks the master schedules with `command_endpoint` (#1736).
- 📤 **The Checkmk agent dump matches the official agent.** New Linux `<<<cpu>>>` and `<<<kernel>>>` sections, the full memory data, process owners and exact numbers. `nscp mk install` sets the agent up from the command line (#1719).
- 📊 **Pressure metrics and volume growth.** Linux pressure stall figures, the Windows processor queue and page faults, the average disk queue, and how much each volume grew in the last hour and day, as metrics and as `check_drivesize` keywords (#1710).
- 🖥️ **Hyper-V over-commitment and virtual switches.** `check_hyperv_host` reports CPU and memory over-commitment, the new `check_hyperv_switches` checks every virtual switch, and `check_hyperv_vms` finds duplicate VM names (#1718).
- 🔒 **Security fixes.** A Checkmk dump field read from the OS can no longer forge rows or sections (#1735). The Windows web backend moves to Mongoose 7.24 (#1722).

## 🔍 Detailed changes

### 🧾 Core — the failed-check log

The log is on by default and lives in memory only. Configure it under `[/settings/core/failed checks]`, or in the new folded *Failed-check log settings* card on the *Failed checks* page:

| Key | Meaning |
|-----|---------|
| `enabled`, `max entries`, `statuses` | Whether to keep the log, how many entries (default 50), which states count. |
| `record arguments` | `none`, `safe` (default: thresholds, filter, syntax and what was checked) or `all` (every option, with `password`/`token` values as `***`). |
| `capture metrics`, `capture diagnostics` | Keep the metrics snapshot and the diagnostics tables with each failure. Off by default. |
| `metrics context budget`, `max context size` | Bound what the snapshots may hold (default 4 MiB). The oldest are released first and their failures stay in the log marked *evicted*. |
| `prune metrics`, `prune pattern` | Trim each snapshot: `zeros, empty, duplicates`, or keys containing a text. |

`GET /api/v2/failures` takes `?status=`, `?command=`, `?since=` and `?limit=`. `GET /api/v2/failures/<index>/context` serves the snapshot, and `DELETE` empties the log. The endpoints need the new `failures.list` / `failures.delete` grants, which only the built-in `full` role holds.

### 🔍 Core — diagnostics

`capture diagnostics` keeps small tables with each failure, each switched on in the module that produces it:

| Table | Holds |
|-------|-------|
| `processes.top_cpu`, `processes.top_memory` | Name, pid, CPU share and memory. Never a command line. |
| `services.problems`, `services.events` | Services not running as they should, and the service manager's crash and restart events. |
| `eventlog.errors` | The last critical and error events (Application and System logs, or the journal). |
| `disk.growth_spots` | The size of the temp and log folders, page and swap files, and shadow-copy storage. |
| `failures.recent` | The last failed checks. Always present. |

`GET /api/v2/diagnostics` (new `diagnostics.list` grant) serves the latest snapshot live, and `nscp test` gains a `diagnostics [section]` command. An enrolled agent sends at most one failure-context report per `failure context interval` (default `1h`) to a fleet server that asks for one. Set `failure context = false` under `[/settings/fleet]` to send none.

### 🧊 IcingaAgent — a native Icinga 2 agent (experimental)

The module is not loaded by default and does nothing until `/settings/Icinga/agent` has a `parent host` and a `parent endpoint`. It then connects to an Icinga 2 master or satellite, gets a certificate (straight away with a `ticket`, otherwise after `icinga2 ca sign`), and runs the checks it is sent. CheckCommands import `ifw-api`, the same convention Icinga for Windows uses. Checks run as `IcingaAgent:<parent endpoint>`, so the permission policy decides what the parent may run. `tls version` and `allowed ciphers` tune the connection. Install the master's `ca.crt`, or set `parent fingerprint`, so the first connection is verified too.

### 📤 CheckMKServer — official agent sections and `nscp mk install`

| Section | Change |
|---------|--------|
| `<<<cpu>>>`, `<<<kernel>>>` | New on Linux: load, thread count, `/proc/vmstat` and `/proc/stat`. |
| `<<<mem>>>` | The whole of `/proc/meminfo` on Linux, commit limit and virtual memory on Windows, exact values. |
| `<<<df>>>` | Built by `check_drivesize` on Linux, with inode counts (needs `CheckDisk`). |
| `<<<ps>>>` | The user field holds the process owner. Every Windows process has a command. |
| `<<<services>>>` | Delayed and trigger-start services are `auto`, as the official agent sends them. |
| `<<<check_mk>>>` | `OSType`, `OSName` and `OSVersion`, which become `cmk/os_*` host labels. |

```
nscp mk install --allowed-hosts 10.0.0.5 --local "CPU Load=check_cpu warn=load>80 crit=load>95"
nscp mk show
```

The install command enables `CheckMKServer`, `CheckSystem` and `CheckDisk`, and adds local checks and MRPE entries. A re-run only changes what it is given.

### 📊 Metrics — pressure, volume growth and a Metrics page that explains itself

- **Pressure.** `system.pressure.*` adds the Linux pressure stall figures for CPU, memory and I/O, major faults, and the Windows processor queue length and page faults. `disk.io.<disk>.avg_queue_length` joins the instantaneous queue length on both platforms.
- **Volume growth.** `disk.free.<drive>.used_change_1h` and `_24h` say how much a volume grew, and `check_drivesize` gains the same keywords: `warn=used_change_1h > 2G`. They read `unknown` until the agent has a full hour (or day) of history.
- **Metrics page.** The web UI shows each metric's description, labels, kind and unit (`640.5 GiB`, `34 %`), grouped by module and instance (#1713, #1715).
- **`check_mssql_counters`** gains `latch_wait_ms`, the average latch wait (#1737).

### 🖥️ Windows — Hyper-V and SCVMM

- **`check_hyperv_host`** gains `running_vms`, `vm_vcpus`, `cpu_overcommit`, `memory_assigned`, `physical_memory` and `memory_overcommit`. It now reads the VMs over WMI, so it needs the same rights as `check_hyperv_vms`. When it cannot, `guests_known` is false and `guests_error` says why.
- **`check_hyperv_switches`** is new: `type`, `state`, `health` and `ports` for every virtual switch.
- **`check_hyperv_vms`** gains `name_count` (`critical=name_count > 1`), and `health` reads `degraded`, `minor_failure`, ... instead of `health_10`, `health_15`, ... (#1718).
- **`scripts\check_scvmm_hosts.ps1`** is a new sample script that checks every host System Center VMM manages (#1720).

### 🛰️ Fleet and core

- **Poll interval bounds.** `poll interval`, `min poll interval` and `max poll interval` under `[/settings/fleet]` bound how often the host polls, whatever the server asks for (#1729).
- **Stored module state is per module.** `nsclient.db` used to share one namespace between modules. Each module (or alias) now owns its entries, and existing sessions and bookmarks are carried over on first start (#1726).
- **`[/settings/core]` keys are known.** A misspelled key there now gets a warning naming the key it resembles, and `nscp settings --validate` fails on it (#1731).
- **No longer experimental:** `check_single_file`, `check_disk_io`, `check_disk_health`, `check_tcp`, `check_dns`, `check_http`, `check_connections`, `check_ntp_offset`, `check_nscp_update` and the `NSCANgClient` module (#1714).

### 🔒 Security

- **Checkmk dump injection.** A line break in a process command line, a mountpoint or a service name could end a row early and pose as another row or a whole section. Control characters are now replaced with a space (#1735).
- **Mongoose 7.24.** The Windows web backend no longer silently ignores headers past the 30th. A request with more is now refused (#1722).
- **OpenSSL 3.5.10.** The twelve November OpenSSL CVEs that scanners flag against the bundled 3.5.9 are not reachable through NSClient++. The notice lists why for each.

### 🐛 Bug fixes

- **`check_http` and `check_nsclient_web_online` honour `timeout=`.** Neither applied it, so a server that accepted the connection and never answered held the check forever (#1707).
- **`check_patch_age`.** A host with no install dates reported age `-1`, which looked freshly patched. `age` is now `unknown`, with a new `age_known` flag (#1734).
- **`check_service`** no longer fails every call on a service whose configuration the agent's account cannot read, and the Checkmk `<<<services>>>` section stays.
- **Windows Update search.** The patch collector could crash when a search was aborted while Windows Update was finishing it. The search now runs to completion on its own thread (#1725).
- **Scheduler `report` lists** accept spaces and any case: `report = critical, warning` used to submit only criticals.
- **Settings.** Setting a key to an empty value from a module or script now stores the empty value instead of deleting the key. Lua and Python gain `remove_key()`. A fleet `timeout = 0` and negative sizes are refused.
- **Module listing.** An unloaded `.zip` module bundle now shows in the full module listing, the REST module list and the web UI (#1727).

### 📦 Packaging

- **check_nsclient 1.2.0** is bundled on Windows and Linux. It adds `nsclient failures`, which reads the failed-check log and the context kept with each failure, `fleet explain`, which asks a fleet server to explain an error, and `nrpe`, which runs a check over NRPE the way `check_nrpe` does.

## ⚠️ Upgrade notes

The full list is on the [upgrading page](https://nsclient.org/docs/setup/upgrading/), and the security fixes are on the [security notices page](https://nsclient.org/docs/security/notices/).

- **Checkmk sites:** run service discovery on hosts monitored through NSClient++. The memory service moves to Checkmk's own memory check, new CPU services appear, and process rules that match on the user now see the owner. On Linux, enable `CheckDisk` to keep `<<<df>>>`. A Lua line object set with `line:set_line(...)` now sends an embedded line break as a space.
- **Custom roles:** the failed-check log needs `failures.list` (`failures.delete` to clear), and diagnostics need `diagnostics.list`.
- **`check_hyperv_vms` `health`:** filters on `health_0`, `health_10`, `health_15` or `health_30` must use `unknown`, `degraded`, `minor_failure` or `non_recoverable_error`.
- **`check_patch_age`:** replace `age < 0` or `age = -1` with `age_known = 0`.
- **`nscp settings --validate`** now fails on a misspelled key under `[/settings/core]`. Fix the spelling it suggests.
- **Scripts that wrote an empty string to reset a key** should call `remove_key()` instead.
- **Windows web server behind a proxy:** a request with more than 30 headers is now dropped. Trim what the proxy forwards if requests start failing.
- **Downgrading** after the first start loses stored module state once: web sessions log out and log bookmarks start over.

## Download

[You can download the new version from GitHub](https://github.com/mickem/nscp/releases/0.27.0){ .md-button }

// Michael Medin

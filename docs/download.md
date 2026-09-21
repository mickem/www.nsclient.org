---
hide:
  - navigation
  - toc
---

# Download

Everything is published on GitHub. Pick the piece you need — the **agent** goes
on the machines you want to monitor, the **fleet server** goes on one host and
configures all of them, and the **command line client** goes wherever you want
to drive them from.

<div class="downloads" markdown="1">
<div class="download-card" markdown="1">

## :material-server: NSClient++

The monitoring agent. Install it on every machine you want to monitor — it
answers NRPE, check_nt, check_mk and REST, and can push results over NSCA,
NRDP, Icinga 2, Graphite and more.

<p class="download-version">
Latest: <strong data-release="version">latest</strong>
&middot; released <span data-release="date">recently</span>
&middot; <a href="https://github.com/mickem/nscp/releases" data-release="notes-link">release notes</a>
</p>

[:material-download: Download NSClient++](https://github.com/mickem/nscp/releases/latest){ .md-button .md-button--primary data-release="download-link" }

**Which file?**

- :fontawesome-brands-windows: **Windows** —
  [64-bit](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-x64.msi" } ·
  [32-bit](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-Win32.msi" } ·
  [ARM64](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-ARM64.msi" data-release-optional="self" } ·
  [XP / 2003](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-Win32-legacy-xp.msi" }
- :fontawesome-brands-ubuntu: **Debian / Ubuntu** —
  [x86-64](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-ubuntu-24.04-amd64.deb" } ·
  [arm64](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-ubuntu-24.04-arm64.deb" }
- :fontawesome-brands-raspberry-pi: **Raspberry Pi OS / Debian 13** —
  [arm64](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-debian-trixie-arm64.deb" data-release-optional="li" }
- :fontawesome-brands-redhat: **RHEL / Rocky / Alma 9** —
  [x86-64](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-rocky-9-x86_64.rpm" } ·
  [arm64](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-rocky-9-aarch64.rpm" }
- :fontawesome-brands-redhat: **RHEL / Rocky / Alma 10** —
  [x86-64](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-rocky-10-x86_64.rpm" } ·
  [arm64](https://github.com/mickem/nscp/releases/latest){ data-release="asset" data-release-asset="NSCP-$version-rocky-10-aarch64.rpm" }

The links point at the files of the latest release, and a platform only
appears when that release actually carries a file for it — **Windows on ARM**
and **Raspberry Pi** arrived in 0.22.0, so they are missing from anything
older. The [package matrix](https://github.com/mickem/nscp#which-package-to-download)
lists every artifact with the distributions it is tested on.

<!-- @formatter:off -->
!!! note "Two things to know about the ARM builds"
    The Windows **ARM64** MSI ships without `PythonScript` and does not bundle
    the Visual C++ runtime, so install
    [vc_redist.arm64.exe](https://aka.ms/vs/17/release/vc_redist.arm64.exe)
    first on a fresh machine. The **Raspberry Pi** package is 64-bit only — a
    Pi 3 or newer running Raspberry Pi OS 64-bit, or Debian 13 arm64 in
    general — and comes without the managed (C#) plugin API.
<!-- @formatter:on -->

- [Quick Start](docs/quick-start.md) — installed and checking in 10 minutes
- [Installation guide](docs/setup/installing.md) — MSI options and silent install
- [Upgrading](docs/setup/upgrading.md) — what to check between your version and this one
- [Security notices](docs/security/notices.md) — advisories and hardening changes, by version
- [Supported platforms](docs/setup/supported-platforms.md)
- [Source: mickem/nscp](https://github.com/mickem/nscp)

</div>
<div class="download-card" markdown="1">

## :material-server-network: NSClient Fleet

The control plane. One server holds the configuration for a whole estate,
hands each host the part that applies to it, and shows you what every host is
actually running. Agents enroll themselves and poll — nothing is pushed.

<p class="download-version">
Latest: <strong data-release="version" data-release-repo="fleet">latest</strong>
&middot; released <span data-release="date" data-release-repo="fleet">recently</span>
&middot; <a href="https://github.com/mickem/nsclient-fleet-server/releases" data-release="notes-link" data-release-repo="fleet">release notes</a>
</p>

[:material-download: Download NSClient Fleet](https://github.com/mickem/nsclient-fleet-server/releases/latest){ .md-button .md-button--primary data-release="download-link" data-release-repo="fleet" }

**Which file?**

| Host | File |
|------|------|
| Linux, x86-64 | `nsclient-fleet-x86_64-unknown-linux-musl` |
| Linux, arm64 | `nsclient-fleet-aarch64-unknown-linux-musl` |
| Windows, 64-bit | `nsclient-fleet-x86_64-pc-windows-msvc.exe` |
| Windows on ARM | `nsclient-fleet-aarch64-pc-windows-msvc.exe` |
| Docker | `ghcr.io/mickem/nsclient-fleet:latest` |

One static binary and a SQLite file — no runtime, no database server. Each
release also carries `SHA256SUMS`, a `nsclient-fleet.service` unit and
`bootstrap-vm.sh`, which sets up a fresh Linux VM end to end.

- [NSClient Fleet documentation](docs/fleet/index.md) — what it is and how it fits together
- [Running it in Docker](docs/fleet/docker.md) — the fastest way to try it
- [Installing on Linux](docs/fleet/linux-install.md) · [on Windows](docs/fleet/windows-install.md)
- [Enrolling your agents](docs/setup/fleet.md) — the agent side of the round trip
- [Source: mickem/nsclient-fleet-server](https://github.com/mickem/nsclient-fleet-server)

</div>
<div class="download-card" markdown="1">

## :material-console: check_nsclient

The command line client for the agent's [REST API](docs/api/rest/index.md). One
self-contained binary that runs checks, edits settings, reads the log and
manages modules on a local or remote agent — and doubles as a Nagios check
plugin, so your monitoring server can poll agents over HTTPS.

<p class="download-version">
Latest: <strong data-release="version" data-release-repo="check_nsclient">latest</strong>
&middot; released <span data-release="date" data-release-repo="check_nsclient">recently</span>
&middot; <a href="https://github.com/mickem/check_nsclient/releases" data-release="notes-link" data-release-repo="check_nsclient">release notes</a>
</p>

[:material-download: Download check_nsclient](https://github.com/mickem/check_nsclient/releases/latest){ .md-button .md-button--primary data-release="download-link" data-release-repo="check_nsclient" }

**Which file?**

- :fontawesome-brands-linux: **Linux** —
  [x86-64](https://github.com/mickem/check_nsclient/releases/latest){ data-release="asset" data-release-repo="check_nsclient" data-release-asset="check_nsclient-$version-linux-x64" } ·
  [arm64](https://github.com/mickem/check_nsclient/releases/latest){ data-release="asset" data-release-repo="check_nsclient" data-release-asset="check_nsclient-$version-linux-arm64" }
- :fontawesome-brands-windows: **Windows** —
  [64-bit](https://github.com/mickem/check_nsclient/releases/latest){ data-release="asset" data-release-repo="check_nsclient" data-release-asset="check_nsclient-$version-windows-x64.exe" } ·
  [32-bit](https://github.com/mickem/check_nsclient/releases/latest){ data-release="asset" data-release-repo="check_nsclient" data-release-asset="check_nsclient-$version-windows-x86.exe" }

<!-- @formatter:off -->
!!! tip "Already on your Windows agents"
    The NSClient++ MSI installs `check_nsclient.exe` alongside the agent, so you
    only need this download for machines that do **not** run NSClient++ — a
    monitoring server, a container, your own workstation.
<!-- @formatter:on -->

- [check_nsclient documentation](docs/check_nsclient/index.md) — install and command reference
- [Active Checks over the REST API](docs/scenarios/rest-api-checks.md) — using it as a Nagios plugin
- [Source: mickem/check_nsclient](https://github.com/mickem/check_nsclient)

</div>
</div>

## Also on the releases page

**Web UI bundle** — [`NSCP-Web-<version>.zip`](https://github.com/mickem/nscp/releases/latest){ data-release="asset" },
attached to each NSClient++
release. The Windows MSI bundles the UI inline, so this is only needed on
Linux, where `sudo nscp web install-ui` fetches and unpacks it for you. See
[Installing the web UI bundle](docs/setup/installing.md#installing-the-web-ui-bundle),
including the offline procedure for air-gapped hosts.

## Latest NSClient++ releases

<div id="nscp-releases" class="release-list">
<p class="release-loading">Loading latest releases…</p>
</div>

[All news :material-arrow-right:](news/index.md){ .md-button }
[All releases on GitHub :material-arrow-right:](https://github.com/mickem/nscp/releases){ .md-button }

## Repositories

| Project | What it is | Repository | Releases |
|---------|------------|------------|----------|
| NSClient++ | The monitoring agent | [mickem/nscp](https://github.com/mickem/nscp) | [releases](https://github.com/mickem/nscp/releases) |
| NSClient Fleet | The control plane for a whole estate | [mickem/nsclient-fleet-server](https://github.com/mickem/nsclient-fleet-server) | [releases](https://github.com/mickem/nsclient-fleet-server/releases) |
| check_nsclient | Command line client for the REST API | [mickem/check_nsclient](https://github.com/mickem/check_nsclient) | [releases](https://github.com/mickem/check_nsclient/releases) |
| This site | Documentation for all of the above | [mickem/www.nsclient.org](https://github.com/mickem/www.nsclient.org) | — |

Building from source is covered in
[build.md](https://github.com/mickem/nscp/blob/main/build.md) for the agent, and
in each project's README otherwise.

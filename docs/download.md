# Download

Everything is published on GitHub. Pick the piece you need — the **agent** goes
on the machines you want to monitor, the **command line client** goes wherever
you want to drive them from.

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

| Host | File |
|------|------|
| Windows, 64-bit | `NSCP-<version>-x64.msi` |
| Windows, 32-bit | `NSCP-<version>-Win32.msi` |
| Windows on ARM | `NSCP-<version>-ARM64.msi` |
| Windows XP / 2003 | `NSCP-<version>-Win32-legacy-xp.msi` |
| Debian / Ubuntu | `NSCP-<version>-ubuntu-24.04-<arch>.deb` |
| RHEL / Rocky / Alma | `NSCP-<version>-rocky-<9\|10>-<arch>.rpm` |

The [package matrix](https://github.com/mickem/nscp#which-package-to-download)
lists every artifact with the distributions it is tested on.

- [Quick Start](docs/quick-start.md) — installed and checking in 10 minutes
- [Installation guide](docs/setup/installing.md) — MSI options and silent install
- [Supported platforms](docs/setup/supported-platforms.md)
- [Source: mickem/nscp](https://github.com/mickem/nscp)

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

| Host | File |
|------|------|
| Linux, x86-64 | `check_nsclient-<version>-linux-x64` |
| Linux, arm64 | `check_nsclient-<version>-linux-arm64` |
| Windows, 64-bit | `check_nsclient-<version>-windows-x64.exe` |
| Windows, 32-bit | `check_nsclient-<version>-windows-x86.exe` |

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

**Web UI bundle** — `NSCP-Web-<version>.zip`, attached to each NSClient++
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
| check_nsclient | Command line client for the REST API | [mickem/check_nsclient](https://github.com/mickem/check_nsclient) | [releases](https://github.com/mickem/check_nsclient/releases) |
| This site | Documentation for all of the above | [mickem/www.nsclient.org](https://github.com/mickem/www.nsclient.org) | — |

Building from source is covered in
[build.md](https://github.com/mickem/nscp/blob/main/build.md) for the agent, and
in each project's README otherwise.

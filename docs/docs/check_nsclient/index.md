<!--
  This page is generated. It is maintained in the check_nsclient repository:
  https://github.com/mickem/check_nsclient/blob/main/docs/index.md
  Run scripts/sync-check-nsclient-docs.py to refresh it; edits made here are
  overwritten.
-->

# check_nsclient

`check_nsclient` is a command line client for the NSClient++
[REST API](../api/rest/index.md). It talks to a running agent over
HTTPS and lets you run checks, inspect and change the configuration, read the
log, manage modules and scripts, and read metrics — locally or on a remote
host.

It is a single self-contained binary. Credentials are kept in the operating
system credential store (Windows Credential Manager, macOS Keychain, Secret
Service on Linux), never in a file next to the binary.

## Installation

`check_nsclient` is a single self-contained binary with no runtime
dependencies — installing it is a matter of putting it somewhere on your
`PATH`.

### Windows: bundled with NSClient++

The NSClient++ MSI installs the client alongside the agent, so on a Windows
host that already runs NSClient++ there is nothing to download:

```
C:\Program Files\NSClient++\check_nsclient.exe
```

(Adjust for `INSTALLLOCATION` if you installed elsewhere.) Add that directory
to `PATH` — or run the client by its full path — and skip to
[Prerequisites](#prerequisites).

### Standalone download

For machines that do **not** run the agent — a Nagios server, an admin
workstation, a container — download the binary from the
[releases page](https://github.com/mickem/check_nsclient/releases). This is
also how you get a newer client than the one your agent shipped with, since the
two are released independently.

| Platform     | Asset                                      |
|--------------|--------------------------------------------|
| Linux x86-64 | `check_nsclient-<VERSION>-linux-x64`       |
| Linux arm64  | `check_nsclient-<VERSION>-linux-arm64`     |
| Windows x64  | `check_nsclient-<VERSION>-windows-x64.exe` |
| Windows x86  | `check_nsclient-<VERSION>-windows-x86.exe` |

#### Linux

Download the binary for your architecture, make it executable and put it on the
path. On a monitoring server the plugin directory
(`/usr/lib/nagios/plugins`) is usually the more natural home:

```commandline
$ VERSION=<VERSION>
$ curl -sSLo check_nsclient \
    "https://github.com/mickem/check_nsclient/releases/download/${VERSION}/check_nsclient-${VERSION}-linux-x64"
$ chmod +x check_nsclient
$ sudo install -m 0755 check_nsclient /usr/local/bin/check_nsclient
$ check_nsclient version
```

> **Note**
>
> On Linux the credential store is the Secret Service (`libsecret`), which
> needs a running keyring daemon. A headless monitoring server usually has
> none — see [Where credentials are stored](nsclient.md#where-credentials-are-stored)
> for how that affects unattended use.

#### Windows

Download `check_nsclient-<VERSION>-windows-x64.exe`, rename it to
`check_nsclient.exe` and place it wherever you keep your tools (adding that
directory to `PATH` saves typing). Credentials go into the Windows Credential
Manager, so no further setup is needed.

### Verifying the install

```commandline
$ check_nsclient version
check_nsclient <VERSION>
```

This is the version of the *client*; `check_nsclient nsclient version` reports
the version of the *agent* you are connected to.

## Prerequisites

The agent must have the
[WEBServer](../reference/generic/WEBServer.md) module enabled
and a password set. If you have not done that yet:

```commandline
$ nscp web install --https --password <MY SECURE PASSWORD>
```

## Getting started

Log in once. The API key you get back is stored in the credential store, so
later commands do not need the password:

```commandline
$ check_nsclient nsclient auth login --password <MY SECURE PASSWORD>
Successfully logged in
```

Then check that the agent answers:

```commandline
$ check_nsclient nsclient ping
Successfully pinged NSClient++ version 0.18.0 2026-08-29
```

And run a check:

```commandline
$ check_nsclient nsclient queries execute check_cpu
╭──────────┬───────────────────────────────╮
│ command  │ check_cpu                     │
│ output   │ OK: CPU load is ok.           │
│ total 1m │ 6%, warning: 80, critical: 90 │
│ total 5m │ 2%, warning: 80, critical: 90 │
│ total 5s │ 9%, warning: 80, critical: 90 │
│ result   │ OK                            │
╰──────────┴───────────────────────────────╯
```

## Using it from your monitoring server

Because `queries execute-nagios` prints a plugin line and exits with the Nagios
status code, the binary doubles as a check plugin. Install it on the monitoring
server, log in once per agent, and call it from a command definition:

```
define command {
    command_name    check_nscp_rest
    command_line    /usr/lib/nagios/plugins/check_nsclient nsclient --profile $HOSTNAME$ queries execute-nagios $ARG1$ $ARG2$
}
```

This gives you active checks over the same HTTPS/REST port the web UI uses, so
there is no second protocol (NRPE) and no second port to open. See
[Active checks over the REST API](../scenarios/rest-api-checks.md)
for the full walkthrough, and
[`queries execute-nagios`](nsclient.md#queries-execute-nagios) for the command
itself.

## Command index

| Command | Description |
|---------|-------------|
| [`nsclient ping`](nsclient.md#ping) | Check that the agent is reachable. |
| [`nsclient version`](nsclient.md#version) | Show the agent name and version. |
| [`nsclient auth login`](nsclient.md#auth-login) | Log in and store the credentials. |
| [`nsclient auth status`](nsclient.md#auth-status) | Show who the stored credentials authenticate as. |
| [`nsclient auth refresh`](nsclient.md#auth-refresh) | Fetch a new API key. |
| [`nsclient auth logout`](nsclient.md#auth-logout) | Revoke the key and forget the profile. |
| [`profile list`](profile.md#profile-list) | List the stored profiles. |
| [`profile show`](profile.md#profile-show) | Show one profile. |
| [`profile set-default`](profile.md#profile-set-default) | Choose the default profile. |
| [`profile remove`](profile.md#profile-remove) | Delete a profile locally. |
| [`nsclient queries list`](nsclient.md#queries-list) | List the available checks. |
| [`nsclient queries show`](nsclient.md#queries-show) | Describe one check. |
| [`nsclient queries execute`](nsclient.md#queries-execute) | Run a check. |
| [`nsclient queries execute-nagios`](nsclient.md#queries-execute-nagios) | Run a check with Nagios output and exit code. |
| [`nsclient aliases list`](nsclient.md#aliases-list) | List the query aliases. |
| [`nsclient modules list`](nsclient.md#modules-list) | List modules. |
| [`nsclient modules show`](nsclient.md#modules-show) | Show one module. |
| [`nsclient modules load` / `unload`](nsclient.md#modules-load-unload) | Load or unload a module now. |
| [`nsclient modules enable` / `disable`](nsclient.md#modules-enable-disable) | Change whether a module loads on startup. |
| [`nsclient modules use`](nsclient.md#modules-use) | Load and enable a module. |
| [`nsclient modules upload`](nsclient.md#modules-upload) | Upload and load a module archive. |
| [`nsclient settings status`](nsclient.md#settings-status) | Where the configuration lives and whether it changed. |
| [`nsclient settings list`](nsclient.md#settings-list) | List configured keys. |
| [`nsclient settings descriptions`](nsclient.md#settings-descriptions) | Describe the keys that can be set. |
| [`nsclient settings set`](nsclient.md#settings-set) | Set a key. |
| [`nsclient settings diff`](nsclient.md#settings-diff) | Show unsaved changes. |
| [`nsclient settings delete`](nsclient.md#settings-delete) | Remove a key or a section. |
| [`nsclient settings command`](nsclient.md#settings-command) | save / load / reload the configuration. |
| [`nsclient logs list`](nsclient.md#logs-list) | Read the agent log. |
| [`nsclient logs status`](nsclient.md#logs-status) | Show the error counters. |
| [`nsclient logs reset`](nsclient.md#logs-reset) | Reset the error counters. |
| [`nsclient logs clear`](nsclient.md#logs-clear) | Drop the buffered records. |
| [`nsclient logs add`](nsclient.md#logs-add) | Append a record to the log. |
| [`nsclient scripts list-runtimes`](nsclient.md#scripts-list-runtimes) | List the script runtimes. |
| [`nsclient scripts list`](nsclient.md#scripts-list) | List the scripts of a runtime. |
| [`nsclient scripts show`](nsclient.md#scripts-show) | Show a script definition. |
| [`nsclient scripts add`](nsclient.md#scripts-add) | Upload a script. |
| [`nsclient scripts delete`](nsclient.md#scripts-delete) | Remove a script definition. |
| [`nsclient metrics show`](nsclient.md#metrics-show) | Read the collected metrics. |
| [`nsclient metrics openmetrics`](nsclient.md#metrics-openmetrics) | Read them in Prometheus format. |
| [`nsclient metadata list`](nsclient.md#metadata-list) | List the metadata resources. |
| [`nsclient metadata counters`](nsclient.md#metadata-counters) | List the performance counters (Windows). |
| [`nsclient metadata channels`](nsclient.md#metadata-channels) | List the submission channels. |
| [`nsclient events list`](nsclient.md#events-list) | Read the event store. |
| [`nsclient events clear`](nsclient.md#events-clear) | Drain the event store. |
| [`nsclient tags show`](nsclient.md#tags-show) | Show the agent tags. |
| [`nsclient client`](nsclient.md#interactive-client) | Open the interactive terminal UI. |

## Command structure

Every command that talks to an agent lives under `nsclient`:

```
check_nsclient [GLOBAL OPTIONS] nsclient [CONNECTION OPTIONS] <COMMAND> [ARGS]
```

Two commands do **not** talk to an agent and therefore sit at the top level:

| Command                    | Description                                       |
|----------------------------|---------------------------------------------------|
| `check_nsclient version`   | Version of `check_nsclient` itself.               |
| `check_nsclient profile …` | Manage stored [profiles](profile.md) locally.    |

> **Note**
>
> `check_nsclient version` reports the version of the *client*, while
> `check_nsclient nsclient version` reports the version of the *agent* it
> connects to.

## Global options

These come *before* the sub command.

| Option                    | Description                                                                    |
|---------------------------|--------------------------------------------------------------------------------|
| `--output <FORMAT>`       | `text` (default), `json`, `yaml` or `csv`. See [output formats](#output-formats). |
| `--output-style <STYLE>`  | Table style for text output: `rounded` (default), `markdown` or `blank`.       |
| `--output-long`           | Show every column, including the ones hidden by default.                       |
| `-d`, `--debug`           | Print each request and response status to stderr. Repeat (`-dd`) to also dump error response bodies. |
| `--wsl`                   | Use the WSL workaround when storing credentials (see [Authentication](nsclient.md#wsl)). |
| `-h`, `--help`            | Show help. Works on every sub command.                                         |

## Connection options

These come after `nsclient` and control how the agent is reached.

| Option                  | Default       | Description                                          |
|-------------------------|---------------|------------------------------------------------------|
| `-p`, `--profile <ID>`  | default profile | Which stored [profile](profile.md) to use.        |
| `-t`, `--timeout-s <N>` | `30`          | Request timeout in seconds.                          |
| `-A`, `--user-agent <S>`| `nscp-client` | User agent to send.                                  |

```commandline
$ check_nsclient nsclient --profile prod --timeout-s 5 ping
Successfully pinged NSClient++ version 0.18.0 2026-08-29
```

## Output formats

Every command supports `--output`. Use `text` for humans and `json`/`yaml` for
scripts — the structured formats keep nested data (metadata, performance data,
pagination) that the table has to flatten or hide.

=== "text (default)"

    ```commandline
    $ check_nsclient nsclient version
    ╭─────────┬───────────────────╮
    │ name    │ NSClient++        │
    │ version │ 0.18.0 2026-08-29 │
    ╰─────────┴───────────────────╯
    ```

=== "json"

    ```commandline
    $ check_nsclient --output json nsclient version
    {
      "name": "NSClient++",
      "version": "0.18.0 2026-08-29"
    }
    ```

=== "yaml"

    ```commandline
    $ check_nsclient --output yaml nsclient version
    name: NSClient++
    version: 0.18.0 2026-08-29
    ```

=== "csv"

    ```commandline
    $ check_nsclient --output csv nsclient version
    name,NSClient++
    version,0.18.0 2026-08-29
    ```

The `markdown` table style is handy when you want to paste the result into a
ticket or a wiki page:

```commandline
$ check_nsclient --output-style markdown nsclient version
| name    | NSClient++        |
| version | 0.18.0 2026-08-29 |
```

### Hidden columns

Wide tables hide their least interesting columns so the output fits in a
terminal. `--output-long` (global) or `--long` (on the commands that have it)
brings them back; `--output json` always contains everything.

```commandline
$ check_nsclient nsclient logs list --size 2 --long
╭───────┬──────────────────────┬───────────────────────────────────────────────────┬──────┬───────────────────────────────────────────────────────╮
│ level │ date                 │ file                                              │ line │ message                                               │
├───────┼──────────────────────┼───────────────────────────────────────────────────┼──────┼───────────────────────────────────────────────────────┤
│ debug │ 2026-Aug-30 15:47:23 │ /__w/nscp/nscp/service/plugins/plugin_manager.cpp │ 966  │ Executing command is target for: CheckExternalScripts │
│ debug │ 2026-Aug-30 15:47:23 │ /__w/nscp/nscp/service/plugins/plugin_manager.cpp │ 1014 │ Executing command in: CheckExternalScripts            │
╰───────┴──────────────────────┴───────────────────────────────────────────────────┴──────┴───────────────────────────────────────────────────────╯
```

## Exit codes

| Code  | Meaning                                                                     |
|-------|-----------------------------------------------------------------------------|
| `0`   | Success.                                                                    |
| `1`   | The command failed (connection refused, not authenticated, server error, …). |
| `0-3` | For [`queries execute-nagios`](nsclient.md#queries-execute-nagios) the Nagios status of the check itself. |

Errors are printed on stderr, so `--output json` on stdout stays parseable:

```commandline
$ check_nsclient nsclient --profile nope ping
Error: NSClient++ profile 'nope' not found.
```

## Troubleshooting

Use `-d` to see the requests as they are made — it goes to stderr and therefore
never corrupts json/yaml/csv on stdout:

```commandline
$ check_nsclient -d nsclient ping
[debug] Debug output enabled (level 1)
[debug] GET https://127.0.0.1:8443/api/v2/info
[debug] 200 OK from api/v2/info
Successfully pinged NSClient++ version 0.18.0 2026-08-29
```

`-dd` additionally dumps the body of error responses, which is where
NSClient++ puts its explanation.

<!--
  This page is generated. It is maintained in the check_nsclient repository:
  https://github.com/mickem/check_nsclient/blob/main/docs/nsclient.md
  Run scripts/sync-check-nsclient-docs.py to refresh it; edits made here are
  overwritten.
-->

# nsclient

Everything `check_nsclient` does against a running agent lives under the
`nsclient` sub command:

```
check_nsclient [GLOBAL OPTIONS] nsclient [CONNECTION OPTIONS] <COMMAND> [ARGS]
```

The [global options](index.md#global-options) (output format, debugging) and
the [connection options](index.md#connection-options) (`--profile`,
`--timeout-s`, `--user-agent`) are described on the
[overview page](index.md), as are the [output formats](index.md#output-formats)
and [exit codes](index.md#exit-codes) every command shares.

## Checking the connection

### ping

Confirms the agent is reachable and prints its version as a single line:

```commandline
$ check_nsclient nsclient ping
Successfully pinged NSClient++ version 0.18.0 2026-08-29
```

### version

The same information as a table (and, in json/yaml/csv, as data):

```commandline
$ check_nsclient nsclient version
╭─────────┬───────────────────╮
│ name    │ NSClient++        │
│ version │ 0.18.0 2026-08-29 │
╰─────────┴───────────────────╯
```

## Authentication

`check_nsclient nsclient auth …` obtains and manages the credentials used to
talk to an agent. Logging in stores an API key (and the password used to renew
it) in the operating system credential store and creates a
[profile](profile.md) describing the server.

### auth login

Authenticates against the agent, stores the API key it hands back and creates
(or replaces) a profile.

```
check_nsclient nsclient auth login [OPTIONS] [ID]
```

| Argument / option       | Default                    | Description                                             |
|-------------------------|----------------------------|---------------------------------------------------------|
| `[ID]`                  | `default`                  | Profile to store the credentials under.                 |
| `--url <URL>`           | `https://localhost:8443`   | Base URL of the agent.                                   |
| `--username <USER>`     | `admin`                    | User to authenticate as.                                 |
| `--password <PASSWORD>` | prompted                   | Password. Can also come from `CHECK_NSCLIENT_PASSWORD`.  |
| `--insecure`            | off                        | Do not validate the TLS certificate.                     |
| `--ca <FILE>`           | system store               | CA bundle to validate the certificate against.           |

```commandline
$ check_nsclient nsclient auth login --password <MY SECURE PASSWORD>
Successfully logged in
```

The first profile you create becomes the default, so subsequent commands need
no `--profile`.

#### Keeping the password out of your shell history

`--password` is optional. When it is omitted the password is read from the
`CHECK_NSCLIENT_PASSWORD` environment variable, and if that is unset you are
prompted for it (the input is not echoed):

```commandline
$ check_nsclient nsclient auth login
Password:
Successfully logged in
```

Both alternatives keep the password out of your shell history and out of the
process list.

#### TLS certificates

NSClient++ generates a self-signed certificate on install, which no CA trusts.
You therefore have to either point at a CA bundle or accept the certificate as
it is:

```commandline
# validate against a CA bundle (recommended)
$ check_nsclient nsclient auth login --ca "C:\Program Files\NSClient++\security\windows-ca.pem"

# ...or skip validation entirely
$ check_nsclient nsclient auth login --insecure
```

Without either, the login fails:

```commandline
$ check_nsclient nsclient auth login --password <PASSWORD>
Error: Failed to login: Failed to login: error sending request for url (https://localhost:8443/api/v2/login): client error (Connect): invalid peer certificate: UnknownIssuer
```

See
[Web interface](../setup/web-interface.md#using-check_nsclient-command)
for how to get a certificate browsers and clients trust.

#### Remote agents

Point `--url` at another host and give the profile a name:

```commandline
$ check_nsclient nsclient auth login prod --url https://prod-01.example.com:8443 --password <PASSWORD>
Successfully logged in
$ check_nsclient nsclient --profile prod ping
Successfully pinged NSClient++ version 0.18.0 2026-08-29
```

### auth status

Shows who the stored credentials authenticate as, and confirms they still work.
This is the cheapest way to verify a profile without side effects.

```commandline
$ check_nsclient nsclient auth status
╭───────────────┬────────────────────────╮
│ profile       │ default                │
│ url           │ https://127.0.0.1:8443 │
│ username      │ admin                  │
│ user          │ admin                  │
│ authenticated │ true                   │
╰───────────────┴────────────────────────╯
```

`username` is what the profile logs in as; `user` is who the server says you
are. In json:

```commandline
$ check_nsclient --output json nsclient auth status
{
  "profile": "default",
  "url": "https://127.0.0.1:8443",
  "username": "admin",
  "user": "admin",
  "authenticated": true
}
```

The command fails when the credentials are not accepted, so it can be used as a
health check:

```commandline
$ check_nsclient nsclient --profile prod auth status || echo "re-authentication needed"
```

### auth refresh

Fetches a new API key using the stored password and replaces the old one.

```commandline
$ check_nsclient nsclient auth refresh
Token successfully refreshed
```

You rarely need this: an expired key is renewed automatically on the next
request, provided the password is still in the credential store. Use `refresh`
when you want the renewal to happen at a predictable moment, for example from
a scheduled job.

### auth logout

Revokes the API key on the server and removes the profile together with its
stored credentials.

```commandline
$ check_nsclient nsclient auth logout default
Successfully logged out
```

Revoking on the server matters: without it the key would remain valid until it
expired, even though it was gone from your machine.

If the agent cannot be reached, or has already forgotten the key, the local
credentials are still removed and the problem is reported as a warning:

```
Warning: could not revoke the token on the server: Invalid response status from api/v2/login: 500 Internal Server Error
Successfully logged out
```

### Where credentials are stored

| Platform | Store                        |
|----------|------------------------------|
| Windows  | Windows Credential Manager   |
| macOS    | Keychain                     |
| Linux    | Secret Service (`libsecret`) |

Two entries are written per profile: `<id>_token` (the API key) and
`<id>_password` (used to renew the key). `auth logout` and
`profile remove` delete both.

<h4 id="wsl">Running under WSL</h4>

WSL has no Secret Service by default, so storing the key fails:

```
Failed to store token in keystore, if you're running under wsl try specifying: check_nsclient --wsl
```

`--wsl` switches to a keyring target that works there. Pass it on every
invocation, not just the login.

## Queries

Queries are the check commands the agent exposes — `check_cpu`,
`check_drivesize` and so on. `check_nsclient nsclient queries …` lists them and
runs them remotely, which makes it a convenient way to try out a check before
wiring it into your monitoring system.

The full list of available checks is in the
[reference](../reference/index.md).

### queries list

```commandline
$ check_nsclient nsclient queries list
╭───────────────────────────┬───────────────────────────┬──────────────╮
│ name                      │ title                     │ plugin       │
├───────────────────────────┼───────────────────────────┼──────────────┤
│ check_always_critical     │ check_always_critical     │ CheckHelpers │
│ check_cpu                 │ check_cpu                 │ CheckSystem  │
│ check_drivesize           │ check_drivesize           │ CheckDisk    │
│ check_memory              │ check_memory              │ CheckSystem  │
│ check_ok                  │ check_ok                  │ CheckHelpers │
│ check_uptime              │ check_uptime              │ CheckSystem  │
╰───────────────────────────┴───────────────────────────┴──────────────╯
```

`name` is what you pass to `execute`. The description is hidden by default:

| Option    | Description                                                          |
|-----------|----------------------------------------------------------------------|
| `--long`  | Also show the description.                                           |
| `--all`   | Include queries from modules that are not loaded.                    |

```commandline
$ check_nsclient nsclient queries list --long | head -5
```

### queries show

Details for one query:

```commandline
$ check_nsclient nsclient queries show check_cpu
╭─────────────┬──────────────────────────────────────────────────────╮
│ name        │ check_cpu                                            │
│ title       │ check_cpu                                            │
│ description │ Check that the load of the CPU(s) are within bounds. │
│ plugin      │ CheckSystem                                          │
╰─────────────┴──────────────────────────────────────────────────────╯
```

`--output json` additionally carries the query metadata.

### queries execute

Runs a check and renders the result — the message, the performance data and
the status:

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

Each performance counter becomes a row. When a check returns several lines they
are numbered (`output 1`, `output 2`, …) and counters that repeat across lines
get a `(line N)` suffix, so nothing is lost.

`--output json` keeps the structure, which is what you want when a script has
to look at individual values:

```commandline
$ check_nsclient --output json nsclient queries execute check_ok
{
  "command": "check_ok",
  "lines": [
    {
      "message": "No message",
      "perf": {}
    }
  ],
  "result": 0
}
```

> **Note**
>
> `execute` always exits `0` when the request itself succeeded, even if the
> check returned CRITICAL — the status is in the output. Use
> [`execute-nagios`](#queries-execute-nagios) if you want the status as the exit code.

An unknown query is not an error at the transport level; the agent answers with
an UNKNOWN result:

```commandline
$ check_nsclient nsclient queries execute no_such_query
╭─────────┬───────────────────────────────────╮
│ command │ no_such_query                     │
│ output  │ Unknown command(s): no_such_query │
│ result  │ UNKNOWN                           │
╰─────────┴───────────────────────────────────╯
```

<h3 id="queries-execute-nagios">queries execute-nagios</h3>

Runs a check and behaves like a Nagios plugin: one line of
`message|performance data` on stdout, and the check status as the **exit code**.

```commandline
$ check_nsclient nsclient queries execute-nagios check_cpu
OK: CPU load is ok.|'total 5s'=9%;80;90 'total 1m'=6%;80;90 'total 5m'=2%;80;90
$ echo $?
0
```

```commandline
$ check_nsclient nsclient queries execute-nagios check_warning message="disk almost full"
disk almost full
$ echo $?
1
```

| Exit code | Status   |
|-----------|----------|
| `0`       | OK       |
| `1`       | WARNING  |
| `2`       | CRITICAL |
| `3`       | UNKNOWN  |

This makes `check_nsclient` usable directly as a check plugin for a monitoring
system that runs checks remotely:

```
define command {
    command_name    check_nscp_remote
    command_line    /usr/bin/check_nsclient nsclient --profile $HOSTNAME$ queries execute-nagios $ARG1$ $ARG2$
}
```

The other output formats work too and still set the exit code, which is handy
when you want both the status and the structured result:

```commandline
$ check_nsclient --output json nsclient queries execute-nagios check_cpu
{
  "command": "check_cpu",
  "lines": [
    {
      "message": "OK: CPU load is ok.",
      "perf": "'total 5s'=6%;80;90 'total 1m'=6%;80;90 'total 5m'=6%;80;90"
    }
  ],
  "result": "OK"
}
$ echo $?
0
```

### Passing arguments

Check arguments are given after the query name, either as `key=value` or as
`--key=value`:

```commandline
$ check_nsclient nsclient queries execute check_cpu --warning="load > 90" --time=5m
$ check_nsclient nsclient queries execute check_cpu warning="load > 90" time=5m
```

Both forms are equivalent — the leading dashes are stripped before the argument
is sent. A bare word becomes a flag with an empty value:

```commandline
$ check_nsclient nsclient queries execute check_drivesize show-all
```

Arguments are passed through verbatim and keep their order, so anything the
check itself accepts works. The
[common options](../reference/common-options.md) page documents
the filter, warning and critical syntax shared by most checks.

> **Note**
>
> Quote values containing spaces or shell metacharacters, as with any other
> command. `--warning="load > 90"` — without the quotes the shell would
> redirect to a file called `90`.

## Aliases

An alias is an admin-defined wrapper around a real check command: a short name
bound to a check plus a fixed set of arguments. They are configured under
`[/settings/check helpers/alias]` (CheckHelpers) or
`[/settings/external scripts/alias]` (CheckExternalScripts).

### aliases list

```commandline
$ check_nsclient nsclient aliases list
╭───────────────────────────┬───────────────────────────┬──────────────────────╮
│ name                      │ title                     │ plugin               │
├───────────────────────────┼───────────────────────────┼──────────────────────┤
│ alias_cpu                 │ alias_cpu                 │ CheckExternalScripts │
│ alias_disk                │ alias_disk                │ CheckExternalScripts │
│ alias_mem                 │ alias_mem                 │ CheckExternalScripts │
│ alias_service             │ alias_service             │ CheckExternalScripts │
│ checkalwaysok             │ CheckAlwaysOK             │ CheckHelpers         │
│ checkversion              │ CheckVersion              │ CheckHelpers         │
╰───────────────────────────┴───────────────────────────┴──────────────────────╯
```

| Option    | Description                                                      |
|-----------|------------------------------------------------------------------|
| `--long`  | Also show the description, which says what the alias expands to.  |
| `--all`   | Include aliases from modules that are not loaded.                |

`--long` is how you find out what an alias actually runs:

```commandline
$ check_nsclient nsclient aliases list --long | grep alias_cpu
│ alias_cpu     │ alias_cpu     │ Alias for: check_cpu     │ CheckExternalScripts │
```

### Running an alias

There is no `aliases execute`. An alias is dispatched by the agent exactly like
a regular query, so run it with [`queries execute`](#queries-execute):

```commandline
$ check_nsclient nsclient queries execute-nagios alias_cpu
OK: CPU load is ok.|'total 5s'=6%;80;90 'total 1m'=6%;80;90 'total 5m'=6%;80;90
```

The json output makes this explicit with a `query_url` pointing at the queries
endpoint:

```commandline
$ check_nsclient --output json nsclient aliases list | jq '.[0]'
{
  "name": "alias_cpu",
  "title": "alias_cpu",
  "description": "Alias for: check_cpu",
  "plugin": "CheckExternalScripts",
  "query_url": "https://127.0.0.1:8443/api/v2/queries/alias_cpu/",
  "metadata": {}
}
```

### Aliases versus queries

[`queries list`](#queries-list) shows the real check commands;
`aliases list` shows the wrappers. A name that appears only in `aliases list`
is an alias, and its `description` tells you which check it delegates to.

Aliases mostly exist for backwards compatibility with the old `check_nt` style
command names, and to give a site its own vocabulary for a check that always
takes the same arguments.

## Modules

Modules are the plugins that give NSClient++ its functionality — the check
commands, the servers and the clients. `check_nsclient nsclient modules …`
lists them and controls whether they are loaded and enabled.

### Loaded versus enabled

Two independent flags decide a module's state:

| Flag      | Meaning                                                                 |
|-----------|-------------------------------------------------------------------------|
| `loaded`  | The module is loaded into the running process right now.                |
| `enabled` | The module is configured to load on startup (`<Module> = enabled`).     |

You can load a module temporarily without enabling it (it disappears on
restart), or enable one without loading it (it appears on the next restart).
[`use`](#modules-use) does both.

### modules list

Modules that are currently loaded:

```commandline
$ check_nsclient nsclient modules list
╭──────────────────────┬──────────────────────┬─────────┬────────┬───────╮
│ id                   │ title                │ enabled │ loaded │ alias │
├──────────────────────┼──────────────────────┼─────────┼────────┼───────┤
│ CheckDisk            │ CheckDisk            │ true    │ true   │       │
│ CheckExternalScripts │ CheckExternalScripts │ true    │ true   │       │
│ CheckHelpers         │ CheckHelpers         │ true    │ true   │       │
│ CheckSystem          │ CheckSystem          │ true    │ true   │       │
│ LUAScript            │ LUAScript            │ true    │ true   │       │
│ WEBServer            │ WEBServer            │ true    │ true   │       │
│ CommandClient        │ CommandClient        │ false   │ true   │       │
╰──────────────────────┴──────────────────────┴─────────┴────────┴───────╯
```

| Option   | Description                                                                     |
|----------|---------------------------------------------------------------------------------|
| `--all`  | Also list modules that are not loaded. Slower: every module on disk is inspected. |
| `--long` | Also show `description`, `name` and `plugin_id`.                                 |

`--all` is how you find out what else is available:

```commandline
$ check_nsclient nsclient modules list --all
╭──────────────────────┬──────────────────────┬─────────┬────────┬───────╮
│ id                   │ title                │ enabled │ loaded │ alias │
├──────────────────────┼──────────────────────┼─────────┼────────┼───────┤
│ CheckDisk            │ CheckDisk            │ true    │ true   │       │
│ WEBServer            │ WEBServer            │ true    │ true   │       │
│ CheckSecurity        │                      │ false   │ false  │       │
│ NRPEServer           │                      │ false   │ false  │       │
│ Scheduler            │                      │ false   │ false  │       │
│ PythonScript         │                      │ false   │ false  │       │
╰──────────────────────┴──────────────────────┴─────────┴────────┴───────╯
```

Modules that are not loaded have no title or description — the agent only reads
that out of a module once it is loaded.

### modules show

```commandline
$ check_nsclient nsclient modules show CheckSystem
╭─────────────┬────────────────────────────────────────────────────────────────────────────╮
│ id          │ CheckSystem                                                                │
│ name        │ CheckSystem                                                                │
│ title       │ CheckSystem                                                                │
│ description │ Various system related checks, such as CPU load, process state and memory. │
│ enabled     │ true                                                                       │
│ loaded      │ true                                                                       │
│ alias       │                                                                            │
│ plugin_id   │ 3                                                                          │
╰─────────────┴────────────────────────────────────────────────────────────────────────────╯
```

```commandline
$ check_nsclient --output json nsclient modules show CheckSystem
{
  "id": "CheckSystem",
  "name": "CheckSystem",
  "title": "CheckSystem",
  "description": "Various system related checks, such as CPU load, process state and memory.",
  "enabled": true,
  "loaded": true,
  "metadata": {
    "alias": "",
    "plugin_id": "3"
  }
}
```

```commandline
$ check_nsclient nsclient modules show NoSuchModule
Error: Failed to fetch module NoSuchModule: Invalid response status from api/v2/modules/NoSuchModule: 404 Not Found: Module not found: NoSuchModule
```

### modules load / unload

Loads or unloads the module in the **running** agent. The configuration is not
touched, so a restart undoes it:

```commandline
$ check_nsclient nsclient modules load CheckNet
Successfully loaded module CheckNet, you can now interact with it but next time the service is restarted it will be unloaded

$ check_nsclient nsclient modules unload CheckNet
Successfully unloaded module CheckNet
```

Loading a module makes its checks available immediately:

```commandline
$ check_nsclient nsclient modules load CheckNet
$ check_nsclient nsclient queries execute check_tcp host=example.com port=443
```

### modules enable / disable

Changes the **configuration** only. The running agent is not affected until the
module is loaded (or the service restarts):

```commandline
$ check_nsclient nsclient modules enable CheckNet
Successfully enabled module CheckNet, this module will be available if you restart the service or if you load it

$ check_nsclient nsclient modules disable CheckNet
Successfully disabled module CheckNet, this module will not be available if you restart the service
```

> **Note**
>
> `enable` and `disable` write to the in-memory configuration. Run
> [`settings command save`](#settings-command) to persist the change, or it
> is lost on restart.

### modules use

The common case: load the module now *and* enable it for future restarts.

```commandline
$ check_nsclient nsclient modules use CheckNet
Successfully loaded and enabled module CheckNet
```

Equivalent to `modules load` followed by `modules enable`. If the load fails
the enable is not attempted.

### modules upload

Uploads a module archive (a `.zip` [zip module](../extending/zip-modules.md))
and loads it:

```commandline
$ check_nsclient nsclient modules upload MyModule --file ./MyModule.zip
Uploaded and loaded module MyModule
```

The archive is stored as `<module-path>/<ID>.zip` on the agent.

> **Warning**
>
> The uploaded archive is loaded immediately and its code runs as the user the
> NSClient++ service runs as — usually a privileged account. Only upload
> archives you trust, and consider whether the `modules.post` privilege should
> be granted at all.

The agent validates the module name and refuses anything that would escape the
module directory.

A missing file is reported before anything is sent, without contacting the
agent:

```commandline
$ check_nsclient nsclient modules upload MyModule --file missing.zip
Error: Failed to read missing.zip: The system cannot find the file specified. (os error 2)
```

## Settings

`check_nsclient nsclient settings …` reads and changes the agent configuration
— the same tree you would otherwise edit in `nsclient.ini`.

### Changes are in memory until you save

`set` and `delete` change the configuration the running agent holds in memory.
Nothing is written to disk until you run [`settings command save`](#settings-command).
The usual sequence is therefore:

```commandline
$ check_nsclient nsclient settings set --path /settings/WEB/server --key threads --value 20
$ check_nsclient nsclient settings diff          # review
$ check_nsclient nsclient settings command save  # persist
```

### settings status

Where the configuration lives and whether it has unsaved changes:

```commandline
$ check_nsclient nsclient settings status
╭─────────────┬──────────────────────────────────╮
│ context     │ ini:///etc/nsclient/nsclient.ini │
│ type        │ ini                              │
│ has_changed │ false                            │
╰─────────────┴──────────────────────────────────╯
```

`has_changed: true` means there are changes that `save` has not yet written.

### settings list

Lists the keys that are actually set, with their values:

```commandline
$ check_nsclient nsclient settings list --path /modules
╭──────────────────────┬──────────┬─────────╮
│ key                  │ path     │ value   │
├──────────────────────┼──────────┼─────────┤
│ CheckDisk            │ /modules │ enabled │
│ CheckExternalScripts │ /modules │ enabled │
│ CheckHelpers         │ /modules │ enabled │
│ CheckSystem          │ /modules │ enabled │
│ LUAScript            │ /modules │ enabled │
│ WEBServer            │ /modules │ enabled │
╰──────────────────────┴──────────┴─────────╯
```

| Option          | Default | Description                                        |
|-----------------|---------|----------------------------------------------------|
| `--path <PATH>` | (all)   | Only list keys under this path (recursively).      |

Without `--path` the whole store is returned, which on a stock agent is a lot
— filtering is usually what you want.

> **Note**
>
> Values of keys the agent marks sensitive (passwords) are returned as `***`.

### settings descriptions

Every key that *can* be set, with its type, title and default — the reference
for a section:

```commandline
$ check_nsclient nsclient settings descriptions --path /settings/WEB/server
╭───────────────────────────────┬──────────────────────┬──────────┬───────────┬─────────────────────────────────╮
│ key                           │ path                 │ type     │ plugins   │ title                           │
├───────────────────────────────┼──────────────────────┼──────────┼───────────┼─────────────────────────────────┤
│ allow anonymous access        │ /settings/WEB/server │ bool     │ WEBServer │ ALLOW ANONYMOUS ACCESS          │
│ allow insecure                │ /settings/WEB/server │ bool     │ WEBServer │ ALLOW INSECURE (CLEARTEXT HTTP) │
│ allowed hosts                 │ /settings/WEB/server │ string   │ WEBServer │ Allowed hosts                   │
│ auth rate limit block seconds │ /settings/WEB/server │ int      │ WEBServer │ AUTH RATE LIMIT (BLOCK SECONDS) │
│ certificate                   │ /settings/WEB/server │ string   │ WEBServer │ TLS Certificate                 │
│ password                      │ /settings/WEB/server │ password │ WEBServer │ Password                        │
│ port                          │ /settings/WEB/server │ string   │ WEBServer │ Server port                     │
│ threads                       │ /settings/WEB/server │ int      │ WEBServer │ Server threads                  │
╰───────────────────────────────┴──────────────────────┴──────────┴───────────┴─────────────────────────────────╯
```

| Option          | Description                                                     |
|-----------------|-----------------------------------------------------------------|
| `--path <PATH>` | Only describe keys under this path.                             |
| `--samples`     | Include sample keys (templates showing how a section is filled). |
| `--long`        | Also show description, default value, current value and flags.   |

`--long` (or `--output json`) is where the actual documentation is:

```commandline
$ check_nsclient --output json nsclient settings descriptions --path /settings/WEB/server \
    | jq '.[] | select(.key == "threads") | {key, type, default_value, description}'
{
  "key": "threads",
  "type": "int",
  "default_value": "10",
  "description": "The number of threads in the sever response pool."
}
```

### settings set

Sets a single key:

```commandline
$ check_nsclient nsclient settings set --path /settings/doc-demo --key sample --value demo
Updated /settings/doc-demo/sample
```

All three options are required. The change is in memory only until you
[save](#settings-command).

### settings diff

Everything that changed since the last save — the review step before you
persist:

```commandline
$ check_nsclient nsclient settings diff
╭─────────────┬────────────────────┬────────┬───────────┬───────────╮
│ change_type │ path               │ key    │ old_value │ new_value │
├─────────────┼────────────────────┼────────┼───────────┼───────────┤
│ added       │ /settings/doc-demo │ sample │           │ demo      │
│ path_added  │ /settings/doc-demo │        │           │           │
╰─────────────┴────────────────────┴────────┴───────────┴───────────╯
```

`change_type` is one of `added`, `removed`, `modified`, `path_added` or
`path_removed`. Adding a key in a section that did not exist yet reports both
the key and the section, as above.

When there is nothing to save:

```commandline
$ check_nsclient nsclient settings diff
No unsaved changes
```

| Option          | Description                              |
|-----------------|------------------------------------------|
| `--path <PATH>` | Only show changes under this path.       |

The `is_sensitive` column is hidden by default; sensitive values are redacted
to `***` by the agent. `--output json` also reports a `count`:

```commandline
$ check_nsclient --output json nsclient settings diff --path /settings/doc-demo
{
  "entries": [
    {
      "change_type": "added",
      "path": "/settings/doc-demo",
      "key": "sample",
      "old_value": "",
      "new_value": "demo",
      "is_sensitive": false
    }
  ],
  "count": 1
}
```

### settings delete

Removes a single key:

```commandline
$ check_nsclient nsclient settings delete --path /settings/doc-demo --key sample
Removed 1 key(s) from /settings/doc-demo/sample
```

Or a whole section, which has to be asked for explicitly:

```commandline
$ check_nsclient nsclient settings delete --path /settings/doc-demo --all-keys
Removed 1 key(s) from /settings/doc-demo
```

Exactly one of `--key` or `--all-keys` is required, so a section can never be
wiped by forgetting an argument:

```commandline
$ check_nsclient nsclient settings delete --path /settings/doc-demo
error: the following required arguments were not provided:
  <--key <KEY>|--all-keys>
```

### settings command

Drives the configuration store itself:

| Action   | Effect                                                        |
|----------|---------------------------------------------------------------|
| `save`   | Write the in-memory configuration to disk.                    |
| `load`   | Re-read the configuration from disk, discarding unsaved changes. |
| `reload` | Ask the service to reload (modules are restarted).            |

```commandline
$ check_nsclient nsclient settings command save
Executed Save command
```

> **Note**
>
> `load` discards unsaved changes — check [`diff`](#settings-diff) first. `reload`
> restarts modules, which briefly interrupts servers such as NRPE or the web
> interface you are talking to.

### A complete example

Raise the number of web server threads and make it permanent:

```commandline
$ check_nsclient nsclient settings descriptions --path /settings/WEB/server --long \
    | grep threads
$ check_nsclient nsclient settings set --path /settings/WEB/server --key threads --value 20
Updated /settings/WEB/server/threads
$ check_nsclient nsclient settings diff
╭─────────────┬──────────────────────┬─────────┬───────────┬───────────╮
│ change_type │ path                 │ key     │ old_value │ new_value │
├─────────────┼──────────────────────┼─────────┼───────────┼───────────┤
│ added       │ /settings/WEB/server │ threads │           │ 20        │
╰─────────────┴──────────────────────┴─────────┴───────────┴───────────╯
$ check_nsclient nsclient settings command save
Executed Save command
$ check_nsclient nsclient settings command reload
Executed Reload command
```

## Logs

The agent keeps its recent log records in memory and exposes them over the API.
`check_nsclient nsclient logs …` reads that buffer, reports the error counters
and can clear both.

This is the fastest way to find out why a check or a module misbehaves without
opening a shell on the host.

### logs list

```commandline
$ check_nsclient nsclient logs list --size 3
╭───────┬──────────────────────┬───────────────────────────────────────────────────────────────╮
│ level │ date                 │ message                                                       │
├───────┼──────────────────────┼───────────────────────────────────────────────────────────────┤
│ debug │ 2026-Aug-30 15:45:17 │ Using certificate: /usr/lib/nsclient/security/certificate.pem │
│ debug │ 2026-Aug-30 15:45:17 │ Loading webserver on port: 8443                               │
│ debug │ 2026-Aug-30 15:45:17 │ Starting plugin: LUAScript                                    │
╰───────┴──────────────────────┴───────────────────────────────────────────────────────────────╯
```

| Option            | Default | Description                                       |
|-------------------|---------|---------------------------------------------------|
| `--page <N>`      | `1`     | Page to read.                                     |
| `--size <N>`      | `50`    | Records per page.                                 |
| `--level <LEVEL>` | (all)   | Only records of this level.                       |
| `--long`          | off     | Also show the source file and line.               |

> **Note**
>
> The agent rejects `--size 1` with `400 Bad Request`; use `2` or more.

Filter to the interesting records:

```commandline
$ check_nsclient nsclient logs list --level error --size 20
```

`--long` adds where the record came from, which is what you want when reporting
a problem:

```commandline
$ check_nsclient nsclient logs list --size 2 --long
╭───────┬──────────────────────┬───────────────────────────────────────────────────┬──────┬───────────────────────────────────────────────────────╮
│ level │ date                 │ file                                              │ line │ message                                               │
├───────┼──────────────────────┼───────────────────────────────────────────────────┼──────┼───────────────────────────────────────────────────────┤
│ debug │ 2026-Aug-30 15:47:23 │ /__w/nscp/nscp/service/plugins/plugin_manager.cpp │ 966  │ Executing command is target for: CheckExternalScripts │
│ debug │ 2026-Aug-30 15:47:23 │ /__w/nscp/nscp/service/plugins/plugin_manager.cpp │ 1014 │ Executing command in: CheckExternalScripts            │
╰───────┴──────────────────────┴───────────────────────────────────────────────────┴──────┴───────────────────────────────────────────────────────╯
```

In json the pagination is included, so a script knows whether more pages
follow:

```commandline
$ check_nsclient --output json nsclient logs list --size 2
{
  "content": [
    {
      "level": "debug",
      "date": "2026-Aug-30 15:47:23",
      "file": "/__w/nscp/nscp/service/plugins/plugin_manager.cpp",
      "line": 966,
      "message": "Executing command is target for: CheckExternalScripts"
    },
    {
      "level": "debug",
      "date": "2026-Aug-30 15:47:23",
      "file": "/__w/nscp/nscp/service/plugins/plugin_manager.cpp",
      "line": 1014,
      "message": "Executing command in: CheckExternalScripts"
    }
  ],
  "page": 1,
  "pages": 26,
  "limit": 2,
  "count": 52
}
```

### logs status

The aggregated error counters — a cheap health check:

```commandline
$ check_nsclient nsclient logs status
╭────────────┬──────────────────────────────────────────╮
│ errors     │ 1                                        │
│ last_error │ Failed to execute command on CheckSystem │
╰────────────┴──────────────────────────────────────────╯
```

`errors` counts the errors logged since the counters were last reset, and
`last_error` is the most recent one. On a healthy agent:

```commandline
$ check_nsclient nsclient logs status
╭────────────┬───╮
│ errors     │ 0 │
│ last_error │   │
╰────────────┴───╯
```

This maps nicely onto a monitoring check of the agent itself:

```commandline
$ errors=$(check_nsclient --output json nsclient logs status | jq .errors)
$ [ "$errors" -eq 0 ] || echo "WARNING: $errors error(s) in the NSClient++ log"
```

### logs reset

Resets the counters `status` reports. The buffered records are kept:

```commandline
$ check_nsclient nsclient logs reset
Successfully reset log status
```

Use it after you have acknowledged a problem, so the next `status` reflects
only new errors.

### logs clear

Drops the buffered records. The counters are unaffected:

```commandline
$ check_nsclient nsclient logs clear
Cleared 23 log record(s)
```

| Command | Clears records | Resets counters |
|---------|----------------|-----------------|
| `reset` | no             | yes             |
| `clear` | yes            | no              |

Clearing before reproducing a problem gives you a buffer that contains only the
relevant records:

```commandline
$ check_nsclient nsclient logs clear
$ check_nsclient nsclient queries execute check_that_misbehaves
$ check_nsclient nsclient logs list --size 50 --long
```

### logs add

Appends a record to the agent log:

```commandline
$ check_nsclient nsclient logs add --message "reboot scheduled by maintenance script"
Log record added
```

| Option              | Default          | Description                            |
|---------------------|------------------|----------------------------------------|
| `--message <TEXT>`  | (required)       | The message to log.                    |
| `--level <LEVEL>`   | `info`           | `debug`, `info`, `warning` or `error`. |
| `--file <NAME>`     | `check_nsclient` | Source attributed to the record.       |
| `--line <N>`        | `0`              | Line attributed to the record.         |

Useful for correlating external activity with what the agent was doing:

```commandline
$ check_nsclient nsclient logs add --level warning --message "starting deploy $VERSION"
```

> **Note**
>
> A record logged at `error` level increases the error counter that
> [`status`](#logs-status) reports, and so will show up in any check watching it.

## Scripts

NSClient++ can run external scripts (batch, shell, PowerShell, …) and Lua
scripts as checks. `check_nsclient nsclient scripts …` lists the runtimes, and
reads, uploads and removes script definitions.

See [External scripts](../scenarios/external-scripts.md) for
how scripts are configured and secured.

### Runtimes

A script belongs to a runtime, selected with `--runtime`:

| Key   | Module                 | Description                                     |
|-------|------------------------|-------------------------------------------------|
| `ext` | CheckExternalScripts   | Anything executed on the command line.          |
| `lua` | LUAScript              | Lua scripts running inside NSClient++.          |
| `py`  | PythonScript           | Python scripts running inside NSClient++.       |

Only runtimes whose module is loaded are available.

### scripts list-runtimes

```commandline
$ check_nsclient nsclient scripts list-runtimes
╭──────────────────────┬──────┬──────────────────────╮
│ module               │ name │ title                │
├──────────────────────┼──────┼──────────────────────┤
│ CheckExternalScripts │ ext  │ CheckExternalScripts │
│ LUAScript            │ lua  │ LUAScript            │
╰──────────────────────┴──────┴──────────────────────╯
```

`name` is what you pass to `--runtime`.

### scripts list

The scripts registered as commands in a runtime:

```commandline
$ check_nsclient nsclient scripts list --runtime ext
╭───────────╮
│ script    │
├───────────┤
│ check_doc │
╰───────────╯
```

| Option      | Description                                                                |
|-------------|----------------------------------------------------------------------------|
| `--runtime` | Runtime to list (required).                                                |
| `--all`     | List every script file found on disk, not only those wired up as a command. |

`--all` shows what is available to be turned into a command:

```commandline
$ check_nsclient --output json nsclient scripts list --runtime ext --all
[
  "scripts\\check_60s.bat",
  "scripts\\check_battery.vbs",
  "scripts\\check_files.vbs",
  "scripts\\check_long.bat",
  "scripts\\check_no_rdp.bat",
  "scripts\\check_ok.bat"
]
```

> **Note**
>
> NSClient++ 0.18.0 does not answer the script listing for the `lua` runtime
> and returns `500 No response from module`. Use
> [`settings list --path "/settings/lua/scripts"`](#settings-list) to see the
> configured Lua scripts instead.

### scripts show

Prints the *definition* — the command line that runs when the check is called:

```commandline
$ check_nsclient nsclient scripts show --runtime ext check_doc
scripts\check_doc
```

The definition is a command line, so its first token tells you which file is
executed. The API also accepts that path in place of the command name to return
the file's contents, but only for files the runtime can resolve under its
configured `script root`; otherwise it answers:

```commandline
$ check_nsclient nsclient scripts show --runtime ext "scripts/check_doc"
Error: Failed to fetch script scripts/check_doc (ext): Invalid response status from api/v2/scripts/ext/scripts/check_doc: 500 Internal Server Error: Command returned errors: Script not found: scripts/check_doc
```

Both `/` and `\` work as separators.

### scripts add

Uploads a script and registers it as a command, replacing any existing
definition of the same name:

```commandline
$ check_nsclient nsclient scripts add --runtime ext check_doc.bat --file ./check_doc.bat
Added check_doc as scripts\check_doc.bat
```

| Argument / option | Description                                     |
|-------------------|-------------------------------------------------|
| `<SCRIPT>`        | File name to store the script under.            |
| `--runtime`       | Runtime to add it to (required).                |
| `--file <PATH>`   | Local file to read the script from (required).  |

Note what the confirmation says: the script was stored as
`scripts\check_doc.bat` and registered as the command **`check_doc`** — the
agent keeps the extension for the file and strips it for the command name. So
include the extension in `<SCRIPT>`, and call the check without it:

```commandline
$ check_nsclient nsclient scripts show --runtime ext check_doc
scripts\check_doc.bat
$ check_nsclient nsclient queries execute-nagios check_doc
OK: everything is fine
```

Leaving the extension out stores an extension-less file the agent then cannot
execute:

```commandline
$ check_nsclient nsclient scripts add --runtime ext check_doc --file ./check_doc.bat
Added check_doc as scripts\check_doc
$ check_nsclient nsclient queries execute-nagios check_doc
Failed to execute check_doc: 2: The system cannot find the file specified.
```

> **Note**
>
> On Linux, NSClient++ 0.18.0 stores the definition with a Windows path
> separator (`scripts\check_doc.sh`) whichever name you use, and the agent then
> cannot run it:
>
> ```
> The command (check_doc) returned an invalid return code: 127
> ```
>
> Uploading works, but on Linux configure the command through the
> [settings](#settings) commands or `[/settings/external scripts/scripts]`
> instead, where you control the path.

A missing local file is reported before anything is sent:

```commandline
$ check_nsclient nsclient scripts add --runtime ext check_doc --file missing.sh
Error: Failed to read missing.sh: The system cannot find the file specified. (os error 2)
```

> **Warning**
>
> An uploaded script runs as the user the NSClient++ service runs as. Treat
> `scripts.add` as an ability to execute arbitrary code on the host and grant
> it accordingly.

> **Note**
>
> This endpoint is a convenience: it cannot set per-script arguments or a
> dedicated user. Use the [settings](#settings) commands, or
> `[/settings/external scripts/scripts]` in the configuration, when you need
> that.

### scripts delete

Removes the script definition:

```commandline
$ check_nsclient nsclient scripts delete --runtime ext check_doc
Script definition has been removed don't forget to delete any artifact for: scripts\check_doc
```

As the message says, only the definition goes away — the file itself is left on
disk and has to be removed separately.

The API also accepts a script *file* path here, to delete the file as well, but
just like [`show`](#scripts-show) that only works for files the runtime resolves under
its configured `script root`:

```commandline
$ check_nsclient nsclient scripts delete --runtime ext "scripts/check_doc"
Error: Failed to delete script scripts/check_doc (ext): Invalid response status from api/v2/scripts/ext/scripts/check_doc: 500 Internal Server Error: Command returned errors: Script not found: scripts/check_doc
```

> **Note**
>
> Removing a definition changes the in-memory configuration. Run
> [`settings command save`](#settings-command) to make it permanent,
> otherwise the script reappears on the next restart or `settings command load`.

## Metrics

NSClient++ collects system metrics continuously — CPU, memory, disk space and
disk I/O — independently of any check. `check_nsclient nsclient metrics …`
reads the current values, either as data or in the Prometheus/OpenMetrics text
format.

See [Prometheus scraping](../scenarios/prometheus.md) for
setting the agent up as a scrape target.

### metrics show

Every metric as a key/value table:

```commandline
$ check_nsclient nsclient metrics show
╭─────────────────────────────────┬────────────────────╮
│ disk.io._Total.queue_length     │ 0                  │
│ disk.io._Total.percent_idle_time│ 100                │
│ system.cpu.total.idle           │ 94.06491968367467  │
│ system.cpu.total.kernel         │ 1.7618464190929828 │
│ system.cpu.total.total          │ 5.935080316325317  │
│ system.cpu.total.user           │ 4.173233897232334  │
│ system.mem.physical.%           │ 73                 │
│ system.mem.physical.avail       │ 4389036032         │
│ system.mem.physical.total       │ 16554041344        │
│ system.mem.physical.used        │ 12165005312        │
╰─────────────────────────────────┴────────────────────╯
```

The list is long — a container reports one entry per mount point and per block
device — so filtering is usually what you want:

```commandline
$ check_nsclient nsclient metrics show | grep system.mem
```

`--output json` keeps the native types (numbers stay numbers), which is what a
script should consume:

```commandline
$ check_nsclient --output json nsclient metrics show | jq '."system.mem.physical.%"'
73
```

> **Note**
>
> For the first few seconds after the agent starts, before CheckSystem has
> completed a collection cycle, the endpoint returns an empty body and the
> command reports:
>
> ```
> Error: Failed to fetch metrics: Empty response from api/v2/metrics (the server may still be starting up, try again shortly)
> ```

<h3 id="metrics-openmetrics">metrics openmetrics</h3>

The same values in the OpenMetrics/Prometheus text exposition format, printed
verbatim:

```commandline
$ check_nsclient nsclient metrics openmetrics
system_cpu_core_0.idle 97.0626
system_cpu_core_0.user 0.586332
system_cpu_core_0.kernel 2.35111
system_cpu_core_0.total 2.93744
system_cpu_core_1.idle 98.8019
system_cpu_core_1.user 0.59802
```

This is the format a scraper expects, so it can be piped straight into one:

```commandline
$ check_nsclient nsclient metrics openmetrics > /var/lib/node_exporter/nscp.prom
```

The body is passed through unchanged in every output format — `--output json`
does not turn it into JSON, because it is not.

> **Note**
>
> A Prometheus server would normally scrape `/api/v2/openmetrics` directly
> rather than go through this command. It is here for ad-hoc inspection and for
> hosts a scraper cannot reach, where a cron job can push the file instead.

### Which one to use

| Use case                                | Command                 |
|-----------------------------------------|-------------------------|
| Look at a value by hand                 | `metrics show`          |
| Feed a script (jq, PowerShell, …)       | `--output json metrics show` |
| Feed Prometheus, or a textfile collector| `metrics openmetrics`   |

## Metadata

The metadata commands describe what the agent *can* do rather than what it is
doing right now: which performance counters exist on the host, and which
submission channels have a listener. Use them to discover what to configure.

### metadata list

The available metadata resources:

```commandline
$ check_nsclient nsclient metadata list
╭──────────┬────────────────────────────────┬─────────────────────────────────────────────────╮
│ name     │ title                          │ url                                             │
├──────────┼────────────────────────────────┼─────────────────────────────────────────────────┤
│ counters │ Performance counters           │ https://127.0.0.1:8443/api/v2/metadata/counters │
│ channels │ Registered submission channels │ https://127.0.0.1:8443/api/v2/metadata/channels │
╰──────────┴────────────────────────────────┴─────────────────────────────────────────────────╯
```

More resources may be added in future releases, so this index is the reliable
way to see what an agent offers.

### metadata counters

The Windows performance counters (PDH) discovered on the host — the values you
can hand to `check_pdh`:

```commandline
$ check_nsclient nsclient metadata counters
╭─────────────────────────────────────────────────┬──────╮
│ name                                            │ type │
├─────────────────────────────────────────────────┼──────┤
│ \Processor Information(_Total)\% Processor Time │      │
│ \Memory\Available Bytes                         │      │
│ \PhysicalDisk(_Total)\Avg. Disk Queue Length    │      │
╰─────────────────────────────────────────────────┴──────╯
```

A real host has thousands of them, and the names follow the Windows display
language — on a Swedish Windows they come back in Swedish. Searching is
therefore the usual reason to run this:

```commandline
$ check_nsclient --output json nsclient metadata counters | jq -r '.[]' | grep -i "processor time"
```

> **Note**
>
> NSClient++ 0.18.0 returns a plain list of counter paths, so the `type` column
> is empty. The client also accepts the richer `{name, type}` form described in
> the [API documentation](../api/rest/metadata.md) should a
> later release start sending it.

Then use it in a check:

```commandline
$ check_nsclient nsclient queries execute check_pdh "counter=\\Processor(_Total)\\% Processor Time"
```

> **Note**
>
> This is a Windows feature and needs the CheckSystem module. On Linux the
> agent has no PDH subsystem and the command fails:
>
> ```
> Error: Failed to fetch performance counters: Invalid response status from api/v2/metadata/counters: 500 Internal Server Error: No response from module, is the CheckSystem module loaded?
> ```
>
> Enumerating every counter on a Windows host can take a long time. Raise the
> timeout if the default is not enough:
> `check_nsclient nsclient --timeout-s 300 metadata counters`.

See [Performance counters (PDH)](../scenarios/counters.md) for
what to do with them.

### metadata channels

The submission channels modules have registered. A channel is the target name a
passive check, a scheduled job or an external script submits its result to; the
agent then dispatches the payload to the listening module.

```commandline
$ check_nsclient nsclient metadata channels
╭────────┬───────────────────────────╮
│ name   │ plugins                   │
├────────┼───────────────────────────┤
│ nsca   │ NSCAClient                │
│ submit │ Op5Client, GraphiteClient │
╰────────┴───────────────────────────╯
```

`plugins` is a list because more than one module can listen on the same
channel, as `submit` shows above; every submission is then delivered to all of
them.

A stock agent has no submission clients loaded and therefore no channels — the
table is empty until you enable something like
[NSCAClient](../reference/client/NSCAClient.md) or
[GraphiteClient](../reference/client/GraphiteClient.md).

This is how you verify that a passive monitoring setup is wired up before
sending anything:

```commandline
$ check_nsclient --output json nsclient metadata channels | jq -r '.[].name'
nsca
submit
```

> **Note**
>
> The built-in pseudo-channels handled by the core itself — `noop` (discard)
> and `log` (write to the agent log) — are not listeners and do not appear
> here, but remain valid submission targets.

## Events

The agent buffers notable occurrences — event log hits, real-time filter
matches — in an event store. `check_nsclient nsclient events …` reads and
drains it, which lets a poller collect what happened without keeping a
connection open.

### events list

Shows the buffered events without removing them:

```commandline
$ check_nsclient nsclient events list
╭───────┬──────────────────────┬──────────┬─────────────────────────────────────────╮
│ index │ date                 │ event    │ data                                    │
├───────┼──────────────────────┼──────────┼─────────────────────────────────────────┤
│ 1     │ 2026-Aug-30 15:52:03 │ eventlog │ id=7036, source=Service Control Manager │
│ 2     │ 2026-Aug-30 15:52:41 │ eventlog │ id=1074, source=User32                  │
╰───────┴──────────────────────┴──────────┴─────────────────────────────────────────╯
```

| Column  | Meaning                                                              |
|---------|----------------------------------------------------------------------|
| `index` | Position in the store, increasing.                                   |
| `date`  | When the event was recorded.                                         |
| `event` | What produced it, for example `eventlog`.                            |
| `data`  | The event payload, flattened to `key=value` pairs for the table.     |

In json the payload keeps its structure:

```commandline
$ check_nsclient --output json nsclient events list
[
  {
    "index": 1,
    "event": "eventlog",
    "date": "2026-Aug-30 15:52:03",
    "data": {
      "source": "Service Control Manager",
      "id": "7036"
    }
  }
]
```

A stock agent produces no events — the store fills only when something feeds
it, such as [CheckEventLog](../reference/windows/CheckEventLog.md)
real-time filters or
[real-time system monitoring](../scenarios/realtime-monitoring.md).
Until then the list is empty.

### events clear

Drains the store and prints what it removed:

```commandline
$ check_nsclient nsclient events clear
╭───────┬──────────────────────┬──────────┬─────────────────────────────────────────╮
│ index │ date                 │ event    │ data                                    │
├───────┼──────────────────────┼──────────┼─────────────────────────────────────────┤
│ 1     │ 2026-Aug-30 15:52:03 │ eventlog │ id=7036, source=Service Control Manager │
│ 2     │ 2026-Aug-30 15:52:41 │ eventlog │ id=1074, source=User32                  │
╰───────┴──────────────────────┴──────────┴─────────────────────────────────────────╯
```

> **Note**
>
> `clear` is a *drain*, not a discard: the events it returns are gone from the
> agent. Capture the output if you need it — running `clear` and ignoring what
> it prints loses those events permanently.

Because of that, `clear` is really "fetch and acknowledge", which is how you
poll the store without processing anything twice:

```commandline
$ check_nsclient --output json nsclient events clear >> /var/log/nscp-events.jsonl
```

A second run finds nothing:

```commandline
$ check_nsclient --output json nsclient events clear
[]
```

Use [`list`](#events-list) when you only want to look, and `clear` when you are
consuming.

## Tags

Tags are small `name = value` facts an agent reports about the host it runs on
— which drives exist, which operating system it is, whether a particular
product was detected. They are contributed at runtime by the loaded modules and
by the core itself, and are read by the web interface and by fleet
synchronisation.

### tags show

```commandline
$ check_nsclient nsclient tags show
╭────────────┬─────────────────╮
│ drives     │ c:,d:           │
│ os_name    │ Windows 11 24H2 │
│ os_version │ 10.0.26200      │
╰────────────┴─────────────────╯
```

Tags are listed in alphabetical order. Which ones exist depends entirely on
which modules are loaded — CheckDisk contributes `drives`, CheckSystem
contributes the operating system tags, and so on. An agent whose loaded modules
report nothing says so rather than printing an empty table:

```commandline
$ check_nsclient nsclient tags show
No tags set
```

In json the tags are returned as an object, which stays `{}` when there are
none, so a script does not have to special-case the message:

```commandline
$ check_nsclient --output json nsclient tags show
{
  "drives": "c:,d:",
  "os_name": "Windows 11 24H2",
  "os_version": "10.0.26200"
}
```

Reading a single tag:

```commandline
$ check_nsclient --output json nsclient tags show | jq -r .os_name
Windows 11 24H2
```

> **Note**
>
> Tags are read-only over the API and are **not** configuration — there is no
> `tags set`, and nothing you write under `/settings` shows up here. A module
> publishes a tag through the plugin API (`NSAPISetTag`), so the way to add one
> is to load a module that reports it.

### Using tags

Tags are a cheap inventory when you drive several agents from one place:

```commandline
$ for profile in web-01 web-02 db-01; do
>   os=$(check_nsclient --output json nsclient --profile $profile tags show | jq -r '.os_name // "unknown"')
>   echo "$profile runs $os"
> done
```

Because the values come from the agent itself they stay correct without a
separate inventory step — a host that gains a drive reports it on the next
poll.

## Interactive client

`check_nsclient nsclient client` opens a terminal UI connected to an agent: a
live CPU and memory bar chart at the top, a log and output pane in the middle,
and a command prompt at the bottom. It is meant for exploring an agent — trying
checks, watching the log react, loading a module — without retyping a full
command line each time.

```commandline
$ check_nsclient nsclient client
```

`check_nsclient nsclient test` is a legacy alias for the same thing.

### Layout

| Area   | Content                                                                       |
|--------|-------------------------------------------------------------------------------|
| Top    | Bar chart of CPU user, CPU kernel and memory usage, refreshed every 5 seconds. |
| Middle | Command output and the agent log, streamed as it arrives, coloured by level.   |
| Bottom | Command prompt.                                                               |

The bars turn yellow above 50% and red above 80%.

New log records are fetched continuously, so a check that logs an error shows
it immediately underneath the output.

### Commands

Type a command and press ++enter++.

| Command                   | Description                                              |
|---------------------------|----------------------------------------------------------|
| `help`                    | List the available commands.                             |
| `ping`                    | Check that the agent is reachable.                       |
| `version`                 | Show the agent version.                                  |
| `queries` (or `list`)     | List every available check command.                      |
| `query <name> [k=v ...]`  | Run a check.                                             |
| `<name> [k=v ...]`        | Run a check directly — the `query` keyword is optional.  |
| `modules` (or `plugins`)  | List modules with a ✓ for the loaded ones.               |
| `modules load <module>`   | Load a module (also `load <module>`).                    |
| `modules unload <module>` | Unload a module (also `unload <module>`).                |
| `refresh`                 | Re-read the status and the list of available checks.     |
| `history`                 | Show the command history.                                |
| `history clear`           | Empty the history.                                       |
| `history delete <index>`  | Remove one entry.                                        |
| `exit`                    | Leave the client (or press ++esc++).                     |

Any check command can be typed on its own, so the two lines below are
equivalent:

```
query check_cpu warning=90
check_cpu warning=90
```

Arguments use the same `key=value` form as
[`queries execute`](#passing-arguments). Values containing spaces can
be quoted, and `\` escapes the next character:

```
check_drivesize "drive=C:\" warning=used>80%
```

### Editing and history

| Key                          | Action                                  |
|------------------------------|-----------------------------------------|
| ++up++ / ++down++            | Walk through the command history.       |
| ++left++ / ++right++         | Move the cursor (also ++ctrl+b++ / ++ctrl+f++). |
| ++home++ / ++end++           | Jump to the start or end (also ++ctrl+a++ / ++ctrl+e++). |
| ++backspace++ / ++delete++   | Delete a character (also ++ctrl+h++ / ++ctrl+d++). |
| ++enter++                    | Run the command.                        |
| ++esc++                      | Exit.                                   |

The prompt validates as you type: a command the agent knows is marked as valid,
an unknown one as invalid, so a typo is visible before you press ++enter++.

Only commands that parse are recorded. A half-typed line you abandon by
pressing ++up++ is remembered while you browse and restored when you come back
past the newest entry, but it never enters the history.

The history holds the last 30 commands and is stored with the rest of the
client configuration, so it survives between sessions.

### When to use the CLI instead

The interactive client is for exploration. For anything scripted — monitoring
integration, automation, structured output — use the ordinary commands, which
support `--output json` and set meaningful [exit codes](index.md#exit-codes).

<!--
  This page is generated. It is maintained in the check_nsclient repository:
  https://github.com/mickem/check_nsclient/blob/main/docs/profile.md
  Run scripts/sync-check-nsclient-docs.py to refresh it; edits made here are
  overwritten.
-->

# profile

A profile is a stored connection: the URL of an agent, the user to log in as,
how its TLS certificate is validated, and a reference to the credentials in the
operating system credential store. Profiles are created by
[`auth login`](nsclient.md#auth-login); the `profile` command manages them locally and
never contacts a server.

Because these commands are local, they sit at the top level rather than under
`nsclient`:

```
check_nsclient profile <COMMAND> [ID]
```

## profile list

```commandline
$ check_nsclient profile list
╭─────────┬────────────────────────┬──────────┬──────────┬─────────┬───────────┬──────────────╮
│ id      │ url                    │ username │ insecure │ default │ has_token │ has_password │
├─────────┼────────────────────────┼──────────┼──────────┼─────────┼───────────┼──────────────┤
│ default │ https://127.0.0.1:8443 │ admin    │ yes      │ yes     │ yes       │ yes          │
│ prod    │ https://prod-01:8443   │ admin    │ no       │ no      │ yes       │ yes          │
╰─────────┴────────────────────────┴──────────┴──────────┴─────────┴───────────┴──────────────╯
```

| Column         | Meaning                                                                    |
|----------------|----------------------------------------------------------------------------|
| `id`           | Name used with `--profile`.                                                |
| `url`          | Base URL of the agent.                                                     |
| `username`     | User the profile authenticates as.                                         |
| `insecure`     | `yes` when the TLS certificate is not validated.                           |
| `default`      | `yes` for the profile used when `--profile` is omitted.                    |
| `has_token`    | Whether an API key is present in the credential store.                     |
| `has_password` | Whether a password is present (needed to renew the key automatically).     |

The `ca` column is hidden by default; `--output-long` or `--output json` shows
it:

```commandline
$ check_nsclient --output json profile list
[
  {
    "id": "default",
    "url": "https://127.0.0.1:8443",
    "username": "admin",
    "insecure": true,
    "ca": null,
    "default": true,
    "has_token": true,
    "has_password": true
  }
]
```

When nothing is configured:

```commandline
$ check_nsclient profile list
No profiles configured
```

> **Note**
>
> `has_token: true` only means a key is stored, not that it still works. Use
> [`auth status`](nsclient.md#auth-status) to verify it against the server.

## profile show

The same fields for a single profile:

```commandline
$ check_nsclient profile show default
╭──────────────┬────────────────────────╮
│ id           │ default                │
│ url          │ https://127.0.0.1:8443 │
│ username     │ admin                  │
│ insecure     │ true                   │
│ ca           │                        │
│ default      │ true                   │
│ has_token    │ true                   │
│ has_password │ true                   │
╰──────────────┴────────────────────────╯
```

```commandline
$ check_nsclient profile show nope
Error: Profile with id 'nope' does not exist
```

## profile set-default

Chooses the profile used when `--profile` is not given:

```commandline
$ check_nsclient profile set-default prod
Default profile updated
```

The first profile created becomes the default automatically. Removing the
default leaves no default, so every command then needs `--profile` until you
set a new one.

## profile remove

Deletes the profile and its credentials from the credential store:

```commandline
$ check_nsclient profile remove prod
Profile removed
```

> **Note**
>
> `profile remove` is local only — it does **not** revoke the API key on the
> server. Use [`auth logout`](nsclient.md#auth-logout) to do both.

## Working with several agents

Log in once per agent, then select one with `--profile`:

```commandline
$ check_nsclient nsclient auth login web-01 --url https://web-01:8443 --password <PASSWORD>
$ check_nsclient nsclient auth login db-01  --url https://db-01:8443  --password <PASSWORD>

$ for host in web-01 db-01; do
>   echo "== $host"
>   check_nsclient nsclient --profile $host queries execute-nagios check_cpu
> done
```
